import json
import logging
import os
import numpy as np
import pandas as pd

from src.utils.misc.type_handling import inverse_dict


FORMAT_EXTS = {
    "fasta": "fasta",
    "npy": "numpy",
    "csv": "csv",
    "json": "json"
}


def verify_file_type(filepath: str, file_type: str):
    assert file_type in filepath or inverse_dict(FORMAT_EXTS).get(file_type) in filepath, \
        f'File {filepath} is not of type {file_type}'


def determine_file_format(filepath: str) -> str:
    ext = os.path.basename(filepath).split('.')[-1]
    try:
        return FORMAT_EXTS[ext]
    except KeyError:
        if os.path.isfile(filepath):
            raise KeyError(f'Could not determine the file format of file {filepath}: "{ext}" '
                           f'not in acceptable extensions {FORMAT_EXTS.keys()}')
        else:
            raise ValueError(
                f'Attempted to determine file format of an object that is not a file: {filepath}')


def load_json_as_dict(json_pathname: str, process=True) -> dict:
    if not json_pathname:
        return {}
    elif type(json_pathname) == dict:
        jdict = json_pathname
    elif type(json_pathname) == str:
        if os.stat(json_pathname).st_size == 0:
            jdict = {}
        else:
            file = open(json_pathname)
            jdict = json.load(file)
            file.close()
    else:
        raise TypeError(
            f'Unknown json loading input {json_pathname} of type {type(json_pathname)}.')
    if process:
        return process_json(jdict)
    return jdict
    # try:
    #     jdict = json.load(open(json_pathname))
    #     if process:
    #         return process_json(jdict)
    #     return jdict
    # except FileNotFoundError:
    #     logging.error(f'JSON path {json_pathname} not found')
    #     import sys
    #     sys.exit()


def process_dict_for_json(dict_like):
    for k, v in dict_like.items():
        if type(v) == dict:
            v = process_dict_for_json(v)
        elif type(v) == np.bool_:
            dict_like[k] = bool(v)
        elif type(v) == np.ndarray:
            dict_like[k] = v.tolist()
        elif type(v) == np.float32 or type(v) == np.int64:
            dict_like[k] = str(v)
    return dict_like


def process_json(json_dict):
    for k, v in json_dict.items():
        if v == "None":
            json_dict[k] = None
    return json_dict


def write_csv(data: pd.DataFrame, out_path: str, overwrite=False):
    if type(data) == dict:
        data = {k: [v] for k, v in data.items()}
        data = pd.DataFrame.from_dict(data)
    if type(data) == pd.DataFrame:
        if overwrite or not os.path.exists(out_path):
            data.to_csv(out_path, index=None)
        else:
            data.to_csv(out_path, mode='a', header=None, index=None)
    elif type(data) == np.ndarray:
        pd.DataFrame(data).to_csv(out_path, mode='a', header=None, index=None)
    else:
        raise TypeError(
            f'Unsupported: cannot output data of type {type(data)} to csv.')


def write_json(data: dict, out_path: str, overwrite=False):
    data = process_dict_for_json(data)
    with open(out_path, 'w+') as fn:
        try:
            json.dump(data, fp=fn, indent=4)
        except TypeError:
            data = str(data)
            json.dump(data, fp=fn, indent=4)


def write_np(data: np.array, out_path: str, overwrite=False):
    if not overwrite and os.path.exists(out_path):
        return
    np.save(file=out_path, arr=data)
