from functools import reduce
from typing import Dict, List


def sort_by_value(_dict: Dict[str, int]) -> List[str]:
    return sorted(_dict.items(), key=lambda x: x[1], reverse=True)


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )
