from nonebot import on_command, CommandSession
from templates import render
from utils import *

__plugin_name__ = '反馈'
__plugin_usage__ = r'''
查看反馈渠道

直接输入 **反馈** 就行!

w(ﾟДﾟ)w 啊? 有 BUG 吗???
'''


@on_command('反馈', aliases=('feedback', ), only_to_me=False)
async def _(session: CommandSession):
    res = render('feedback')
    await session.send(res)
