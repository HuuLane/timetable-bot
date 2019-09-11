from nonebot import on_command, CommandSession
from utils import log


# @on_command('课表', aliases=('查课'))
@on_command('课表')
async def curriculum(session: CommandSession):
    day = session.get('day', prompt='亲, 你想查询哪天的课呀?')
    # 得到课程信息
    res = await course(day)
    await session.send(res)


@curriculum.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    arg = session.current_arg_text.strip()
    log('用户输入参数', arg)
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if arg:
            session.state['day'] = arg
        return
    if not arg:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('倒是说呀???')
    session.state[session.current_key] = arg


async def course(day: str) -> str:
    return f'今天的课程有 {day}'
