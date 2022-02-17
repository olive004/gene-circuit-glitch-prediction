from functools import partial


class DataManager():
    def __init__(self, source=None, data=None):
        self.data = self.load_data(source) if data is None else data
        self.sample_names = list(self.data.values())

    def load_data(self, source):
        from src.utils.data.data_format_tools.common import determine_data_format
        filepath = source
        data_type = determine_data_format(filepath)
        loader = self.get_loader(data_type)
        return loader(filepath)

    def get_loader(self, data_type):
        if data_type == "fasta":
            from src.utils.data.data_format_tools.manipulate_fasta \
                import load_seq_from_FASTA
            return partial(load_seq_from_FASTA, as_type='dict')
        else:
            raise NotImplementedError(
                "Other filetypes than fasta not supported yet.")

    @property
    def size(self):
        return len(self.data)

    @size.getter
    def size(self):
        return len(self.data)

    @property
    def sample_names(self):
        return self._sample_names

    @sample_names.getter
    def sample_names(self):
        if type(self.data) == dict:
            return list(self.data.keys())
        else:
            import numpy as np
            return list(np.range(len(self.data)))

    @sample_names.setter
    def sample_names(self, value):
        if type(value) == list or type(value) == dict:
            self._sample_names = value
        else:
            raise ValueError(f'Wrong type "{type(value)}" for ' +
                             'setting data sample_names to {value}')

    def __repr__(self) -> str:
        return str(self.data)
