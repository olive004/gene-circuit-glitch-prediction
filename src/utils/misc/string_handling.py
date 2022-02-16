from datetime import datetime
from copy import deepcopy
import random


def generate_str_from_dict(str_dict, length):
    return ''.join(random.choice(list(str_dict.keys())) for n in range(length))


def list_to_str(input_listlike):
    return ''.join(input_listlike)


def make_time_str():
    """Output as 'YEAR_MONTH_DAY_TIME'."""
    now = datetime.now() 
    return now.strftime("%Y_%m_%d_%H%M%S")


def ordered_merge(list1, list2, mask):
    # its = [iter(l) for l in lists]
    # for m in mask:
    #     yield next(its[i])
    list1 = list1 if type(list1) == list else list(list1)
    merged = deepcopy(list1)
    for i, (n,c,m) in enumerate(zip(list1, list2, mask)):
        merged[i] = c if m else n
    return list_to_str(merged)


def remove_special_py_functions(string_list: list) -> list:
    return [s for s in string_list if '__' not in s]
