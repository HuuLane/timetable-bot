# import pdir
from utils.time import now
# def log(o):
#     '''
#     接收一个 object, 打印出来
#     '''
#     keys = list(pdir(o).public)
#     print(keys)


def log(*args, **kwargs):
    print(*args, **kwargs)


def delkey(dict, *keys):
    for k in keys:
        del dict[k]
