import unittest
import numpy as np
from src.utils.system_definition.agnostic_system.base_system import BaseSystem


class TestBaseSystem(unittest.TestCase):

    def test_label_nodes(self):
        circuit = BaseSystem()
        new_labels = list(np.range(len(circuit.graph)))
        circuit.label_nodes(new_labels)
        self.assertEqual(circuit.graph, new_labels, "Re-labelling failed.")


if __name__ == '__main__':
    unittest.main()
