from functools import partial
import os

from fire import Fire

from src.utils.results.experiments import Experiment, Protocol
from src.utils.results.result_writer import ResultWriter
from src.utils.results.visualisation import visualise_data
from src.srv.parameter_prediction.simulator import RawSimulationHandling
from src.srv.sequence_exploration.sequence_analysis import tabulate_mutation_info
from src.utils.data.data_format_tools.common import load_json_as_dict


def main(config=None, data_writer=None):
    # Set configs
    num_mutations = 2
    if config is None:
        config = os.path.join(
            # "scripts", "analyse_mutated_templates", "configs", "logscale", "analyse_templates.json")
            # "scripts", "analyse_mutated_templates", "configs", "logscale", "analyse_mutated_templates_1.json")
            "scripts", "analyse_mutated_templates", "configs", "logscale", "analyse_mutated_templates_2.json")
    config_file = load_json_as_dict(config)

    # Start_experiment
    if data_writer is None:
        data_writer = ResultWriter(purpose='analyse_mutated_templates')

    source_dir = config_file.get('source_dir')
    if config_file.get('preprocessing_func') == 'rate_to_energy':
        preprocessing_func = RawSimulationHandling().rate_to_energy,
    else:
        preprocessing_func = None

    if config_file.get('only_visualise_circuits', False):
        exclude_rows_via_cols = ['mutation_name']
    else:
        exclude_rows_via_cols = []

    plot_grammar = 's' if num_mutations > 1 else ''

    protocols = [
        Protocol(
            partial(tabulate_mutation_info, source_dir=source_dir,
                    data_writer=data_writer),
            req_output=True,
            name='tabulate_mutation_info'
        ),
        Protocol(
            partial(visualise_data, data_writer=data_writer, cols=['interaction_strength'],
                    plot_type='histplot', out_name='interaction_strength_freqs',
                    preprocessor_func=preprocessing_func,
                    exclude_rows_nonempty_in_cols=['mutation_name'],
                    log_axis=config_file.get('log_scale', False),
                    use_sns=True,
                    title='Maximum interaction strength, unmutated circuits',
                    xlabel='Interaction strength', ylabel='Frequency count'),
            req_input=True,
            name='visualise_circuit_interactions'
        ),
        Protocol(
            partial(visualise_data, data_writer=data_writer, cols=['interaction_strength'],
                    plot_type='histplot', out_name='interaction_strength_freqs',
                    preprocessor_func=preprocessing_func,
                    exclude_rows_nonempty_in_cols=exclude_rows_via_cols,
                    log_axis=config_file.get('log_scale', False),
                    use_sns=True,
                    title=f'Maximum interaction strength, {num_mutations} mutation{plot_grammar}',
                    xlabel='Interaction strength', ylabel='Frequency count'),
            req_input=True,
            name='visualise_mutated_interactions'
        ),
        Protocol(
            partial(visualise_data, data_writer=data_writer, cols=['interaction_strength_diff_to_base_circuit'],
                    plot_type='histplot', out_name='interaction_strength_diffs',
                    preprocessor_func=preprocessing_func,
                    exclude_rows_nonempty_in_cols=exclude_rows_via_cols,
                    log_axis=config_file.get('log_scale', False),
                    title=f'Difference btwn circuit and mutated interaction strengths, {num_mutations} mutation{plot_grammar}',
                    xlabel='Interaction strength difference', ylabel='Frequency count'),
            req_input=True,
            name='visualise_interactions_difference',
            skip=config_file.get('only_visualise_circuits', False)
        )
    ]
    experiment = Experiment(config_filepath=config, protocols=protocols,
                            data_writer=data_writer)
    experiment.run_experiment()


if __name__ == "__main__":
    Fire(main)
