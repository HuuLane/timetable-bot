from os import path
import nonebot
import config


nonebot.init(config)
nonebot.load_plugins(
    path.join(path.dirname(__file__), 'plugins'),
    'plugins'
)

bot = nonebot.get_bot()
app = bot.asgi

# run the bot!
# hypercorn bot:app
bot.run()
