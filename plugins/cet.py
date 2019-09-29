from nonebot import on_command, CommandSession
from templates import render
from utils import *
import CET46


@on_command('四六级', aliases=('四级', '六级', 'cet'), only_to_me=False)
async def cet(session: CommandSession):
    arg = session.get('arg')
    # 根据参数, 生成响应信息
    res = await cet_info(arg)
    await session.send(res)


@cet.args_parser
async def _(session: CommandSession):
    '''
    参数解析
    '''
    # 去掉消息首尾的空白符
    arg = session.current_arg_text.strip()
    if arg:
        session.state['arg'] = arg


async def cet_info(arg: str) -> str:
    log('哟, 还有参数呢:', arg)
    remaining = CET46()
    return f'剩余 {remaining} 天!'
