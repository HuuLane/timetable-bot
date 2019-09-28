from .time import *
from .db import *
import json


def log(*args, **kwargs):
    print(*args, **kwargs)


def delkey(dict_, *keys):
    for k in keys:
        del dict_[k]


def load_json(path, default=[]):
    """
    从一个文件中载入数据并转化为 list
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            print(f'读取{path}数据')
            return json.loads(s)
    except FileNotFoundError:
        # 默认 list
        return default
