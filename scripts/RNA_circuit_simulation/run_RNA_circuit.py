from fire import Fire

from src.utils.decorators import time_it
from src.utils.system_definition.configurations import parse_cfg_args
from src.utils.system_definition.specific_systems.RNA_system import RNASystem


@time_it
def main(config_file=None):

    parsed_namespace_args = parse_cfg_args(config_file)

    circuit = RNASystem(parsed_namespace_args)
    circuit.visualise()


if __name__ == "__main__":
    Fire(main)
