

import logging
import os

import numpy as np
from src.srv.io.loaders.data_loader import DataLoader
from src.utils.results.result_writer import ResultWriter
from src.utils.data.data_format_tools.common import load_json_as_dict
from src.utils.misc.io import get_pathnames, isolate_filename
from src.utils.misc.numerical import triangular_sequence
from src.utils.results.experiments import Experiment, Protocol
from src.utils.misc.scripts_io import get_search_dir, get_subprocesses_dirnames, load_experiment_config
from src.utils.misc.string_handling import sort_by_ordinal_number


def main(config=None, data_writer=None):

    if config is None:
        config = os.path.join(
            'scripts', 'stitch_parameter_grid', 'configs', 'base_config.json')
    config_file = load_json_as_dict(config)
    if data_writer is None:
        data_writer = ResultWriter(purpose=config_file[
            'experiment'].get('purpose', 'stitch_parameter_grid'))

    # Load in parameter grids
    config_file, source_dir = get_search_dir(
        config_search_key='source_parameter_dir', config_file=config_file)
    experiment_config = load_experiment_config(source_dir)
    experiment_settings = experiment_config['experiment']
    num_subprocesses = 1
    if experiment_settings['parallelise']:
        num_subprocesses = experiment_settings['num_subprocesses']

    # If there was multithreading, load each parameter_grid one by one from subfolders
    def load_parameter_grids():
        all_parameter_grids = {}
        subprocess_dirs = get_subprocesses_dirnames(source_dir)
        for subprocess_dir in sort_by_ordinal_number(subprocess_dirs):
            parameter_grids = get_pathnames(subprocess_dir, 'npy')
            for parameter_grid in parameter_grids:
                analytic_name = isolate_filename(parameter_grid)
                if analytic_name not in all_parameter_grids.keys():
                    all_parameter_grids[analytic_name] = []
                all_parameter_grids[analytic_name].append(
                    DataLoader().load_data(parameter_grid))
        return all_parameter_grids
    all_parameter_grids = load_parameter_grids()

    # Stitch grids together
    def stitch_grids():
        # Find the starting and ending indices

        a_parameter_grid = all_parameter_grids[list(
            all_parameter_grids.keys())[0]][0]
        matrix_size = np.size(a_parameter_grid)
        num_species = np.shape(a_parameter_grid)[0]
        num_unique_interactions = triangular_sequence(num_species)
        size_interaction_array = np.shape(a_parameter_grid)[-1]

        total_iterations_correct = np.power(
            size_interaction_array, num_unique_interactions)
        total_iterations = matrix_size
        num_iterations = int(total_iterations / num_subprocesses)

        # Iterate through all possible index combinations (corresponding to all possible parameter combinations)
        def make_indices(iteration):
            return tuple([slice(0, num_species)] + [int(np.mod(iteration / np.power(size_interaction_array, unique_interaction),
                                                               size_interaction_array)) for unique_interaction in range(num_unique_interactions)])

        all_iterators = [None] * total_iterations_correct
        for ite in range(total_iterations_correct):
            all_iterators[ite] = make_indices(ite)

        stitched_parameter_grids = {k: np.zeros(
            np.shape(a_parameter_grid)) for k in all_parameter_grids.keys()}
        for analytic_name in stitched_parameter_grids.keys():
            logging.info('\n\n')
            logging.info(analytic_name)

            for ite in range(total_iterations_correct):
                i = int(ite/num_iterations)
                current_grid = all_parameter_grids[analytic_name][i]
                idxs = all_iterators[ite]
                stitched_parameter_grids[analytic_name][idxs] = current_grid[idxs]

            logging.info(
                f'Number of zeros in subprocess matrix: {np.sum(all_parameter_grids[analytic_name][i] == 0)}')
            logging.info(
                f'Number of zeros in stitched matrix: {np.sum(stitched_parameter_grids[analytic_name] == 0)}')
            logging.info(
                f'Difference in zeros: {np.absolute(np.sum(all_parameter_grids[analytic_name][i] == 0) - np.sum(stitched_parameter_grids[analytic_name] == 0))}')
        return stitched_parameter_grids

    # Write full matrices
    def write_all(stitched_parameter_grids, out_type='npy'):
        for analytic_name, grid in stitched_parameter_grids.items():
            data_writer.output(out_type, out_name=analytic_name,
                               data=grid.astype(np.float32), overwrite=True,
                               write_to_top_dir=True)

    # stitched_parameter_grids = stitch_grids()
    # write_all(stitched_parameter_grids)

    experiment = Experiment(config_filepath=config, protocols=[
        Protocol(stitch_grids, req_output=True, name='Stitching grids together'),
        Protocol(write_all, req_input=True, name='Writing stitched grids')],
        data_writer=data_writer)
    experiment.run_experiment()
    
    return config, data_writer
