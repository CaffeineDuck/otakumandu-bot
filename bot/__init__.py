import re
from typing import Sequence

import traceback
import discord
from discord import Intents
from discord.ext import commands
from tortoise import Tortoise

from config import bot_config
from tortoise_config import tortoise_config


class OtakuBot(commands.Bot):
    def __init__(self, command_prefix: str, bot_cogs: Sequence, load_jishaku: bool) -> None:
        super().__init__(
            command_prefix=command_prefix, 
            description='Just a bot to mess with your brains',
            intents = Intents.all()
        )
        self.bot_cogs = bot_cogs
        
        if load_jishaku:
            self.load_extension('jishaku')

        self.load_cogs()
    
    def load_cogs(self) -> None:
        for cog in self.bot_cogs:
            try:
                self.load_extension(cog)
                print(f'Loaded Cog: {cog}')
            except commands.ExtensionError:
                traceback.print_exc()

    async def on_ready(self):
        print('Connecting to database')
        await Tortoise.init(tortoise_config)
        print('Connected to database' + f'\nLogged in with {self.user}')

    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"I am missing the following permissions:\n **{','.join(error.missing_perms)}**"
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"You are missing the following permissions:\n**{','.join(error.missing_perms)}**"
            )
        else:
            title = " ".join(re.compile(r"[A-Z][a-z]*").findall(error.__class__.__name__))
            await ctx.send(
                embed=discord.Embed(
                    title=title, description=str(error), color=discord.Color.red()
                )
            )
            raise error
