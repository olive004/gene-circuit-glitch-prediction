from functools import partial
import logging
from random import random
import numpy as np
from src.utils.data.manage.writer import DataWriter, Tabulated


from src.utils.system_definition.agnostic_system.base_system import BaseSpecies, BaseSystem


class Mutations(Tabulated):

    def __init__(self, mutation_name, template_file, template_species,
                 positions, mutation_types, algorithm='random') -> None:
        self.mutation_name = mutation_name
        self.template_file = template_file
        self.template_species = template_species
        self.mutation_types = mutation_types
        self.positions = positions
        self.count = len(positions)
        self.algorithm = algorithm

    def get_columns(self):
        return list(self.__dict__.keys())


class Evolver():

    mapping = {
        # Mutation idx from parent key to child key
        "A": {
            "C": 0,
            "G": 1,
            "T": 2
        },
        "C": {
            "A": 3,
            "G": 4,
            "T": 5
        },
        "G": {
            "A": 6,
            "C": 7,
            "T": 8
        },
        "T": {
            "A": 9,
            "C": 10,
            "G": 11
        },
        "U": {
            "A": 12,
            "C": 13,
            "G": 14
        }
    }

    def __init__(self, num_mutations, **data_writer_kwargs) -> None:
        self.num_mutations = num_mutations
        self.data_writer = DataWriter(**data_writer_kwargs)

    def mutate(self, system: BaseSystem, algorithm="random"):
        mutator = self.get_mutator(algorithm)
        mutator(system.species)

    def get_mutator(self, algorithm):

        def random_mutator(species: BaseSpecies, species_idx: int):
            positions = np.random.randint(0, species.data.get_data_by_idx(
                species_idx), size=self.num_mutations)
            return positions

        def basic_mutator(species: BaseSpecies, position_generator, species_idx: int = None):
            sequence = species.data.get_data_by_idx(species_idx)
            positions = np.random.randint(0, sequence, size=self.num_mutations)
            positions = position_generator(species, species_idx)
            Mutations(
                mutation_name=species.data.sample_names,
                template_file=species.data.source,
                template_species=sequence,
                mutation_types=self.sample_mutations(sequence, positions),
                positions=positions
            )
            self.write_mutations(Mutations)

        def full_mutator(species: BaseSpecies, sample_mutator_func):
            for sample in range(species.data.sample_names):
                sample_mutator_func(species.data.get_data_by_idx(sample))

        if algorithm == "random":
            return partial(full_mutator, sample_mutator_func=
                partial(basic_mutator, position_generator=random_mutator)
            )
        else:
            return ValueError(f'Unrecognised mutation algorithm choice "{algorithm}"')

    def sample_mutations(self, sequence, positions):
        mutation_types = []
        for p in positions:
            possible_transitions = self.mapping[sequence[p]]
            logging.info(possible_transitions)
            mutation_types.append(random.choice(
                list(possible_transitions.keys())))
        return mutation_types

    def write_mutations(self, mutations: Mutations):
        self.data_writer.
