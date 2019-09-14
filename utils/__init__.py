from utils.time import *


def log(*args, **kwargs):
    print(*args, **kwargs)


def delkey(dict, *keys):
    for k in keys:
        del dict[k]
