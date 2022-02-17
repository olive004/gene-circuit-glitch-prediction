import unittest
import numpy as np
from src.utils.data.data_format_tools.manipulate_fasta import load_seq_from_FASTA


class TestDataFormatting(unittest.TestCase):

    def test_fasta_seq_loading(self):
        seqs = load_seq_from_FASTA(
            "./src/utils/data/example_data/toy_mRNA_circuit.fasta", 
            as_type="dict")
        keys = list(seqs.keys())
        self.assertEqual(keys[0], 'RNA_0', "Re-labelling failed.")


if __name__ == '__main__':
    unittest.main()


