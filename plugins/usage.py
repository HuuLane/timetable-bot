import nonebot
from nonebot import on_command, CommandSession


def plugin_list(plugins):
    # return '\n'.join(f'{i}.\t{p.name}' for i, p in enumerate(plugins))
    ns = (p.name for p in plugins)
    return '\n'.join(sorted(ns, key=len))


@on_command('usage', aliases=['使用帮助', '帮助', '使用方法'])
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '目前支持的功能有：\n\n' + plugin_list(plugins)
        )
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if arg in p.name.lower():
            await session.send(p.usage)
            return
