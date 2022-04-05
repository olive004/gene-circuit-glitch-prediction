from functools import partial
from abc import ABC, abstractmethod
import os
import pandas as pd

from src.utils.data.data_format_tools.manipulate_fasta import write_fasta_file
from src.utils.misc.helper import get_subdirectories
from src.utils.misc.string_handling import make_time_str


class DataWriter():

    def __init__(self, purpose, out_location=None) -> None:
        self.script_dir = os.path.join('scripts')
        self.root_output_dir = os.path.join('data')
        self.exception_dirs = os.path.join('example_data')
        if out_location is None:
            self.write_dir = self.make_location(purpose)
        else:
            self.write_dir = out_location

    def output(self, out_location, out_type, **writer_kwargs): # data_generator, out_type, gen_type, gen_run_count):
        writer = self.get_write_func(out_type, out_location)
        writer(**writer_kwargs)

    def get_write_func(self, out_type, out_location):
        if out_type == "fasta":
            return partial(write_fasta_file, fname=out_location)
        if out_type == "csv":
            pass
        raise ValueError(
            f'No write function available for output of type {out_type}')

    def make_location(self, purpose):

        if purpose in get_subdirectories(self.script_dir) or purpose in self.exception_dirs:
            return os.path.join(self.root_output_dir,
                                purpose,
                                self.generate_location_instance())
        raise ValueError(f'Unrecognised purpose for writing data to {purpose}')

    def generate_location_instance(self):
        return make_time_str()


class Tabulated(ABC):

    def __init__(self) -> None:
        self.column_names = self.get_columns()

    @abstractmethod
    def get_columns(self):
        pass

    def as_table(self):
        return pd.DataFrame(columns=self.column_names)
