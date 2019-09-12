from nonebot import on_command, CommandSession
from utils import log, now


# @on_command('课表', aliases=('查课'))
@on_command('下节课')
async def curriculum(session: CommandSession):
    pattern = session.get('pattern')
    # 根据参数, 生成响应信息
    res = await course(pattern)
    await session.send(res)


@curriculum.args_parser
async def _(session: CommandSession):
    '''
    参数解析
    '''
    # 去掉消息首尾的空白符
    arg = session.current_arg_text.strip()
    log('用户输入参数', arg)
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if arg:
            session.state['pattern'] = arg
        else:
            session.state['pattern'] = None
    # session.state[session.current_key] = arg


async def course(pattern: str) -> str:
    n = now()
    print('now', n)
    if pattern is None:
        return f'随便'
    elif '啰嗦' in pattern:
        r = f'今天是第 {n[0]} 周, 星期 {n[1] + 1}.\n' \
            f'北京时间 {n[2]}:{n[3]}.\n'
        return r
