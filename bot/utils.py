import re

from discord.ext import commands

from .errors import NotValidImageUrl

URL_REGEX = re.compile(
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


class ImageUrl(commands.Converter):
    @classmethod
    async def convert(cls, _: commands.Context, message: str) -> str:
        if not URL_REGEX.match(message):
            NotValidImageUrl()

        return message
