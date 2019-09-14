from models import Subject
from os import path
import nonebot
import config


def init():
    import sys
    arg = 'update'
    if arg in sys.argv:
        # 更新数据库
        Subject.update()


def run_bot():
    nonebot.init(config)
    # say & echo
    # nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()


if __name__ == '__main__':
    init()
    run_bot()
