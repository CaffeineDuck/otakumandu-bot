from config import bot_config
from typing import Optional
import discord
from discord.ext import commands

from bot import OtakuBot
from models import InviteModel

INVITE_ROLE = {str(bot_config.server_id): bot_config.invite_role}
REQUIRED_INVITES = {str(bot_config.server_id): bot_config.invite_req}

class Invite(commands.Cog):
    def __init__(self, bot: OtakuBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self.update_invites(member.guild)

    @commands.Cog.listener()
    async def on_completing_invite_reqs(self, invite: discord.Invite) -> None:
        user = await invite.guild.fetch_member(invite.inviter.id)
        role = invite.guild.get_role(INVITE_ROLE.get(str(invite.guild.id)))
        await user.add_roles(role)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite) -> None:
        await InviteModel.get_or_create(code=invite.code)

    async def handle_user_invites(self, invite: discord.Invite) -> None:
        invite_models = await InviteModel.filter(inviter=invite.inviter.id)
        uses = sum([invite_model.uses for invite_model in invite_models])

        if uses >= REQUIRED_INVITES.get(str(invite.guild.id)):
            self.bot.dispatch("completing_invite_reqs", invite)

    async def update_invites(self, guild: discord.Guild) -> None:
        invites: list[discord.Invite] = await guild.invites()

        for invite in invites:
            invite_model, _ = await InviteModel.get_or_create(
                code=invite.code, inviter=invite.inviter.id
            )

            if invite_model.uses == invite.uses:
                continue

            invite_model.uses = invite.uses
            await invite_model.save()
            await self.handle_user_invites(invite)

    @commands.command(name="fetchinvites")
    @commands.has_permissions(administrator=True)
    async def fetch_invites(self, ctx: commands.Context) -> None:
        async with ctx.typing():
            await self.update_invites(ctx.guild)

            await ctx.send("Invites have been fetched and updated!")

    @commands.command(name='invites')
    async def user_invites(self, ctx:commands.Context, member: Optional[discord.Member]) -> None:
        member = member or ctx.author

        invite_models = await InviteModel.filter(inviter=member.id)
        uses = sum([invite_model.uses for invite_model in invite_models])

        await ctx.send(f'{member} has `{uses}` valid invites!')


def setup(bot: OtakuBot) -> None:
    bot.add_cog(Invite(bot))
