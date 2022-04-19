from datetime import datetime
import logging
from typing import List
from src.utils.data.data_format_tools.common import load_json_as_dict

from src.srv.io.results.writer import DataWriter
from src.utils.misc.type_handling import make_attribute_list


class Protocol():

    def __init__(self, protocol, req_output=False, req_input=False, name='') -> None:
        self.req_output = req_output
        self.req_input = req_input
        self.protocol = protocol
        self.name = name
        self.output = None

    def __call__(self, *input_args):
        if input_args is None:
            output = self.protocol()
        else:
            output = self.protocol(*input_args)
        if self.req_output:
            if output is not None:
                self.output = output
            return output


class Experiment():

    def __init__(self, config_file: str, protocols: List[Protocol], data_writer: DataWriter) -> None:
        
        self.name = 'experiment'
        self.config_file = config_file
        self.start_time = datetime.now()
        self.protocols = protocols
        self.total_time = 0
        self.data_writer = data_writer

    def run_experiment(self):
        out = None
        self.iterate_protocols(self.protocols, out)

        self.total_time = datetime.now() - self.start_time
        self.write_experiment()

    def iterate_protocols(self, protocols, out):
        for protocol in protocols:
            if type(protocol) == Protocol:
                logging.info(protocol.name)
                out = self.call_protocol(protocol, out)
            elif type(protocol) == list and type(out) == list:
                for o in out:
                    self.iterate_protocols(protocols=protocol, out=o)

    def call_protocol(self, protocol, out=None):
        if protocol.req_input:
            out = protocol(out)
        else:
            out = protocol()
        return out

    def write_experiment(self):
        experiment_data = self.collect_experiment()
        self.data_writer.output(out_type='json', out_name=self.name, data=experiment_data)
        
    def collect_experiment(self):
        return {
            "total_time": str(self.total_time),
            "protocols": make_attribute_list(self.protocols, Protocol, 'name'),
            "purpose": self.data_writer.purpose,
            "config_file": self.config_file,
            "config_params": load_json_as_dict(self.config_file)
        }