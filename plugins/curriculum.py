from nonebot import on_command, CommandSession
from templates import render
from utils import *
import Timetable

Timetable.load(**dict(
    subjects='./static/subjects.json',
    routine='./static/routine.json',
))


@on_command('下节课', aliases=('查课', '课表'), only_to_me=False)
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
    log('有人查课啦~', pattern)
    t = Timetable().__dict__
    t.update(dict(
        debug=False,
        now=Timetable.schooltime(),
        now_course=Timetable.now(),
    ))
    return render('human-friendly',  **t)
