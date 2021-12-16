from fire import Fire
import timeit
import sys

from src.utils.decorators import time_it

@time_it
def main(config_args=None):
    circuit = BaseSystem(config_args)
    circuit = construct_system(circuit)
    
    circuit.visualise()

if __name__ == "__main__":
    Fire(main)
