import logging
import os

from bot import OtakuBot
from config import bot_config

os.environ.setdefault("JISHAKU_HIDE", "1")
os.environ.setdefault("JISHAKU_RETAIN", "1")
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")

logging.basicConfig(level=logging.INFO)

cogs = ("bot.cogs.welcome",)

if __name__ == "__main__":
    bot = OtakuBot(bot_config.prefix, cogs, True)
    bot.run(bot_config.bot_token)
