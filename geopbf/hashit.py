# -*- coding: utf-8 -*-

"""
Courtesy of: https://stackoverflow.com/a/64572412/1039510
"""

import collections
import hashlib
import json

def simplify(obj):
    if isinstance(obj, dict):
        return {key: simplify(value) \
            for key,value in collections.OrderedDict(sorted(obj.items())).items()}
    elif isinstance(obj, (list, tuple, set,)):
        return list(sorted(map(simplify, obj)))
    else:
        return str(obj).strip()

def hashit(obj):
    bytes_val = json.dumps(simplify(obj), sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha1(bytes_val.encode()).hexdigest()
