import logging
from src.utils.system_definition.agnostic_system.base_system import BaseSystem, BaseSpecies

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
FORMAT = "%(filename)s:%(funcName)s():%(lineno)i: %(message)s %(levelname)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RNASystem(BaseSystem):
    def __init__(self, config_args):
        super(RNASystem, self).__init__(config_args)

        self.simulator_args = config_args.get("interaction_simulator", {})

        self.species = self.init_species(config_args)
        self.process_species()

        # Rates
        # 2 h^-1 or 30 mins or 1800s - Dilution rate
        cell_dbl_growth_rate = 2 / 3600
        avg_RNA_pcell = 100
        starting_copynumber = 50
        self.transcription_rate = cell_dbl_growth_rate * avg_RNA_pcell

        self.species.copynumbers, \
            self.species.degradation_rates, \
            self.species.creation_rates = self.species.init_matrices(ndims=1, init_type="uniform",
                                                                     uniform_vals=[starting_copynumber,
                                                                                   cell_dbl_growth_rate,
                                                                                   self.transcription_rate])

    def init_species(self, args):
        return RNASpecies(args)

    def process_species(self):
        self.node_labels = self.species.data.sample_names


class RNASpecies(BaseSpecies):
    def __init__(self, config_args):
        super().__init__(config_args)

        molecular_params = config_args.get("molecular_params")
        if molecular_params is None:
            raise ValueError(f'Could not find molecular parameters in config for RNA species. \nArgs: \n{config_args}')

        self.degradation_rates = self.init_matrix(ndims=1, init_type="uniform",
                                                  uniform_val=molecular_params.get("degradation_rates"))
        self.creation_rates = self.init_matrix(ndims=1, init_type="uniform",
                                               uniform_val=molecular_params.get("creation_rates"))
        # self.copynumbers = self.init_matrix(ndims=1, init_type="uniform",
        #                                     uniform_val=5)
        self.copynumbers = None  # For modelling
