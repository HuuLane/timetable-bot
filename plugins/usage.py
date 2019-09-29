import nonebot
from utils import *
from nonebot import on_command, CommandSession


def plugin_list(plugins):
    # return '\n'.join(f'{i}.\t{p.name}' for i, p in enumerate(plugins))
    ns = (p.name for p in plugins)
    return '\n'.join(sorted(ns, key=len))


@on_command('usage', aliases=['查看帮助', '帮助'])
async def usage(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    # 从会话状态（session.state）中获取 arg，如果当前不存在，则询问用户
    prompt = '目前支持的功能有：\n\n' + plugin_list(plugins) + '\n\n回复查看命令说明'
    arg = session.get('arg', prompt=prompt)

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if arg in p.name.lower():
            await session.send(p.usage)
            return
    else:
        await session.send('没有这条命令呀..')


@usage.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    log('stripped_arg:', stripped_arg)
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空, 可以直接返回啦
            session.state['arg'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效参数，则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查看的命令不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
