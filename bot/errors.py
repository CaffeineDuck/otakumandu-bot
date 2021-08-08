from discord.ext import commands


class WelcomeNotConfigured(commands.CommandError):
    def __str__(self) -> str:
        return "Welcome has not been configured yet!"


class WelcomeAlreadyConfigured(commands.CommandError):
    def __str__(self) -> str:
        return "Welcome has been already configured you can't overwrite!"


class NotValidImageUrl(commands.CommandError):
    def __str__(self) -> str:
        return "The image url you provided is not valid!"
