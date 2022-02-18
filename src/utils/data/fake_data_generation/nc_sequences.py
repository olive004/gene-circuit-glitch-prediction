from itertools import permutations
import random
import numpy as np
from functools import partial
from typing import List
from Bio.Seq import Seq

from src.utils.misc.helper import next_wrapper
from src.utils.misc.string_handling import ordered_merge, list_to_str
from src.utils.misc.numerical import nPr, generate_mixed_binary


RNA_POOL = {
    'A': 0.2,
    'C': 0.3,
    'G': 0.3,
    'U': 0.2
}
DNA_POOL = {
    'A': 0.2,
    'C': 0.3,
    'G': 0.3,
    'T': 0.2
}


def generate_str_from_dict(str_dict, length):
    return ''.join(random.choice(list(str_dict.keys())) for n in range(length))


def generate_mutated_template(template: str, mutate_prop, mutation_pool):
    mutate_idxs = np.random.randint(
        len(template), size=int(len(template)*mutate_prop))
    template = list(template)
    for idx in mutate_idxs:
        template[idx] = np.random.choice(
            list(mutation_pool.keys()), p=list(mutation_pool.values()))
    template = ''.join(template)
    return template


def convert_symbolic_complement(real_seq, symbolic_complement):
    comp_seq = str(Seq(real_seq).complement())
    return list_to_str(ordered_merge(real_seq, comp_seq, symbolic_complement))


def generate_mixed_template(template: str, count) -> list:
    # TODO: Generate proper permutations or arpeggiations, 
    # rank by mixedness and similarity. Can use list(permutations())
    # and ranking function in future.
    
    symbolic_complements = generate_mixed_binary(len(template), count)
    seq_permutations = [None] * count
    for i, symb in enumerate(symbolic_complements):
        seq_permutations[i] = convert_symbolic_complement(template, symb)
    return seq_permutations


def generate_split_template(template: str, count) -> list:
    assert count < len(template), \
        f"Desired sequence length {len(template)} too short to accomodate {count} samples."
    template_complement = str(Seq(template).complement())
    fold = max(int(len(template) / count), 1)

    seqs = []  # could preallocate
    for i in range(0, len(template), fold):
        complement = template_complement[i:(i+fold)]
        new_seq = template[:i] + complement + template[(i+fold):]
        seqs.append(new_seq)
    return seqs[:count]


def write_seq_file(seq_generator, fname, stype, count):
    with open(fname, 'w') as f:

        for i in range(count):
            seq_name = '>' + stype + '_' + str(i) + '\n'
            f.write(seq_name)
            f.write(seq_generator() + '\n')


def create_toy_circuit(stype='RNA', count=5, slength=20, protocol="random",
                       proportion_to_mutate=0):
    """ Protocol can be 
    'random': Random sequence generated with weighted characters
    'template_mix': A template sequence is interleaved with complementary characters
    'template_mutate': A template sequence is mutated according to weighted characters
    'template_split': Parts of a template sequence are made complementary

    """
    fname = './src/utils/data/example_data/toy_mRNA_circuit.fasta'
    if stype == 'RNA':
        nucleotide_pool = RNA_POOL
    elif stype == 'DNA':
        nucleotide_pool = DNA_POOL
    else:
        raise NotImplementedError
    template = generate_str_from_dict(nucleotide_pool, slength)
    # template = 'CGCGCGCGCGCGCGCGCGCGCGCCGCGCG'  # Very strong interactions
    # template = 'CUUCAAUUCCUGAAGAGGCGGUUGG'  # Very weak interactions
    if protocol == "template_mutate":
        seq_generator = partial(generate_mutated_template,
                                template=template,
                                mutate_prop=proportion_to_mutate,
                                mutation_pool=nucleotide_pool)
    elif protocol == "template_split":
        sequences = generate_split_template(template, count)
        seq_generator = partial(next_wrapper, generator=iter(sequences))
    elif protocol == "template_mix":
        sequences = generate_mixed_template(template, count)
        seq_generator = partial(next_wrapper, generator=iter(sequences))
    elif protocol == "random":
        seq_generator = partial(generate_str_from_dict,
                                str_dict=nucleotide_pool, slength=slength)
    else:
        seq_generator = partial(generate_str_from_dict,
                                str_dict=nucleotide_pool, slength=slength)
        raise NotImplementedError
    write_seq_file(seq_generator, fname, stype, count)



def main():
    # Testing
    template = 'ACTGTGTGCCCCTAAACCGCGCT'
    count = 10
    seq_permutations = generate_mixed_template(template, count)
    assert len(seq_permutations) == count, 'Wrong sequence length.'
    print(seq_permutations)