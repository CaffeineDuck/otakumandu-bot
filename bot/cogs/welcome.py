import discord
from discord.ext import commands

from bot import OtakuBot
from bot.errors import WelcomeAlreadyConfigured, WelcomeNotConfigured
from bot.utils import ImageUrl
from config import bot_config
from models import WelcomeModel


class Welcome(commands.Cog):
    def __init__(self, bot: OtakuBot):
        self.bot = bot

    async def get_welcome_model(self, ctx: commands.Context) -> WelcomeModel:
        welcome_model = await WelcomeModel.get_or_none(guild_id=ctx.guild.id)
        if not welcome_model:
            raise WelcomeNotConfigured()

        return welcome_model

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if member.guild.id != bot_config.server_id:
            return

        welcome_model = await WelcomeModel.get_or_none(guild_id=member.guild.id)
        if not welcome_model:
            return

        welcome_message = welcome_model.message.format(
            guild=member.guild, member=member
        )
        welcome_channel = self.bot.get_channel(welcome_model.channel)

        embed = discord.Embed(
            title=welcome_model.title,
            description=welcome_message,
            color=welcome_model.color or discord.Color.random(),
        )

        embed.set_footer(
            text=welcome_model.footer_text or discord.Embed.Empty,
            icon_url=welcome_model.footer_image or discord.Embed.Empty,
        )

        if welcome_model.image:
            embed.set_image(url=welcome_model.image)

        if welcome_model.image_thumbnail:
            embed.set_thumbnail(url=welcome_model.image_thumbnail)

        await welcome_channel.send(member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(_, guild: discord.Guild) -> None:
        if guild.id != bot_config.server_id:
            await guild.leave()

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: commands.Context) -> None:
        welcome_model = await self.get_welcome_model(ctx)

        embed = discord.Embed(title="Welcome Configuration", color=welcome_model.color)
        embed.add_field(
            name="Message Channel",
            value=self.bot.get_channel(welcome_model.channel).mention,
            inline=False,
        )
        embed.add_field(
            name="Title",
            value=welcome_model.title,
            inline=False,
        )
        embed.set_footer(
            text=welcome_model.footer_text or discord.Embed.Empty,
            icon_url=welcome_model.footer_image or discord.Embed.Empty,
        )

        if welcome_model.image_thumbnail:
            embed.set_thumbnail(url=welcome_model.image_thumbnail)
        if welcome_model.image:
            embed.set_image(url=welcome_model.image)
        embed.add_field(name="Message String", value=welcome_model.message)

        await ctx.send(embed=embed)

    @welcome.command(name="delete")
    async def welcome_delete(self, ctx: commands.Context) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        await welcome_model.delete()

        await ctx.send("Welcome configuration for this server has been deleted!")

    @welcome.group(name="set", invoke_without_command=True)
    async def welcome_set(_, ctx: commands.Context) -> None:
        await ctx.send_help(ctx.command)

    @welcome_set.command(name="channel")
    async def welcome_set_channel(
        self, ctx: commands.Context, channel: discord.TextChannel
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.channel = channel.id

        await welcome_model.save()
        await ctx.send(f"Welcome model has been updated to {channel.mention}")

    @welcome_set.command(name="message")
    async def welcome_set_message(
        self, ctx: commands.Context, *, welcome_message: str
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.message = welcome_message

        await welcome_model.save()

        await ctx.send("Welcome message has been updated!")

    @welcome_set.command(name="color")
    async def welcome_set_color(
        self, ctx: commands.Context, color: discord.Color
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.color = color.value
        await welcome_model.save()

        await ctx.send(f"Welcome color has been updated to {color}")

    @welcome_set.command(name="title")
    async def welcome_set_title(self, ctx: commands.Context, *, title: str) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.title = title
        await welcome_model.save()

        await ctx.send(f"Welcome color has been updated")

    @welcome_set.group(name="footer", invoke_without_command=True)
    async def welcome_set_footer(_, ctx: commands.Context) -> None:
        await ctx.send_help(ctx.command)

    @welcome_set_footer.command(name="text")
    async def welcome_set_footer_text(self, ctx: commands.Context, text: str) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.footer_text = text

        await welcome_model.save()
        await ctx.send(f"Welcome model footer text has been updated!")

    @welcome_set_footer.command(name="image")
    async def welcome_set_footer_image(
        self, ctx: commands.Context, image_url: ImageUrl
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.footer_image = image_url

        await welcome_model.save()
        await ctx.send(f"Welcome model footer image has been updated!")

    @welcome_set.group(name="image", invoke_without_command=True)
    async def welcome_set_image(ctx: commands.Context) -> None:
        await ctx.send_help(ctx.command)

    @welcome_set_image.command("main")
    async def welcome_set_image_main(
        self, ctx: commands.Context, image_url: ImageUrl
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.image = image_url

        await welcome_model.save()
        await ctx.send("Welcome model image has been updated!")

    @welcome_set_image.command("thumbnail")
    async def welcome_set_image_thumbnail(
        self, ctx: commands.Context, image_url: ImageUrl
    ) -> None:
        welcome_model = await self.get_welcome_model(ctx)
        welcome_model.thumbnail = image_url

        await welcome_model.save()
        await ctx.send("Welcome model thumbnail image has been updated!")

    @welcome_set.command(name="full")
    async def welcome_set_full(
        self,
        ctx: commands.Context,
        welcome_channel: discord.TextChannel,
        welcome_title: str,
        welcome_message: str,
    ) -> None:
        if await WelcomeModel.exists(guild_id=ctx.guild.id):
            raise WelcomeAlreadyConfigured()

        await WelcomeModel.create(
            guild_id=ctx.guild.id,
            channel=welcome_channel.id,
            message=welcome_message,
            title=welcome_title,
        )
        await ctx.send("Welcome has been configured now!")

    @welcome.command(name="test")
    async def welcome_test(self, ctx: commands.Context, member: discord.Member) -> None:
        self.bot.dispatch("member_join", member)
        await ctx.send("Member Join event has been dispatched!")


def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
