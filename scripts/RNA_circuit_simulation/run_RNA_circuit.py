from fire import Fire

from src.utils.decorators import time_it
from src.utils.system_definition.configurations import parse_kwargs
from src.utils.system_definition.specific_systems import RNASystem


@time_it
def main(config_file=None):

    kwargs = parse_kwargs(config_file)

    circuit = RNASystem(kwargs)
    circuit.visualise()


if __name__ == "__main__":
    Fire(main)
