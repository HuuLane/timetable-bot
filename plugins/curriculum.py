from nonebot import on_command, CommandSession
from templates import render
from utils import *
from models import Subject

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
    print('有人查课啦~ now', n)
    next_class = Subject(n)
    info = next_class.info
    print('info:', info)
    if info is None:
        return '恭喜本学期完课啦~~'
    if pattern is None:
        return f'{info["name"]}, 地点: {info["place"]}'
    elif '啰嗦' in pattern:
        args = dict(
            now=pretty_now(n),
            info=info,
            week=next_class.week,
            day=day_num_to_cn(int(next_class.day)),
            class_ordinal=next_class.class_ordinal,
        )
        return render('next_verbose', **args)
