from nonebot import on_command, CommandSession
from templates import render
from utils import *
import CET46

__plugin_name__ = '四六级倒计时'
__plugin_usage__ = r'''
返回四六级倒计时~

直接输入 **cet** 就行!

w(ﾟДﾟ)w 啊? 就这几天啦???
'''


@on_command('四六级', aliases=('四级', '六级', 'cet'), only_to_me=False)
async def cet(session: CommandSession):
    # 根据参数, 生成响应信息
    res = await cet_info()
    await session.send(res)


async def cet_info() -> str:
    # time remaining
    r = CET46()
    if r > 0:
        pass
    return f'剩余 {r} 天!'
