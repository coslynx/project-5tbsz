import discord
from discord.ext import commands

from utils.helpers import create_embed

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Checks the bot's latency.")
    async def ping(self, ctx):
        """Checks the bot's latency."""
        await ctx.send(embed=create_embed(title="Pong!", description=f"Latency: {round(self.bot.latency * 1000)}ms"))

    @commands.command(name="help", help="Displays the bot's available commands.")
    async def help(self, ctx):
        """Displays the bot's available commands."""
        embed = create_embed(title="Help", description="Here are the available commands:")
        for command in self.bot.commands:
            embed.add_field(name=f"!{command.name}", value=command.help, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", help="Displays information about the current server.")
    async def serverinfo(self, ctx):
        """Displays information about the current server."""
        server = ctx.guild
        embed = create_embed(title=f"Server Info: {server.name}", description=f"**Members:** {server.member_count}\n**Created At:** {server.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", help="Displays information about a specified user.")
    async def userinfo(self, ctx, user: discord.Member = None):
        """Displays information about a specified user."""
        if user is None:
            user = ctx.author
        embed = create_embed(title=f"User Info: {user.name}#{user.discriminator}", description=f"**ID:** {user.id}\n**Joined At:** {user.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name="kick", help="Kicks a user from the server (requires appropriate permissions).")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user from the server (requires appropriate permissions)."""
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=create_embed(title="Kicked", description=f"{member.mention} has been kicked from the server."))
        except discord.Forbidden:
            await ctx.send(embed=create_embed(title="Error", description="I do not have permission to kick members."))

    @commands.command(name="ban", help="Bans a user from the server (requires appropriate permissions).")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a user from the server (requires appropriate permissions)."""
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=create_embed(title="Banned", description=f"{member.mention} has been banned from the server."))
        except discord.Forbidden:
            await ctx.send(embed=create_embed(title="Error", description="I do not have permission to ban members."))

    @commands.command(name="mute", help="Mutes a user in the server (requires appropriate permissions).")
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mutes a user in the server (requires appropriate permissions)."""
        try:
            await member.edit(mute=True, reason=reason)
            await ctx.send(embed=create_embed(title="Muted", description=f"{member.mention} has been muted in the server."))
        except discord.Forbidden:
            await ctx.send(embed=create_embed(title="Error", description="I do not have permission to mute members."))

    @commands.command(name="unmute", help="Unmutes a user in the server (requires appropriate permissions).")
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmutes a user in the server (requires appropriate permissions)."""
        try:
            await member.edit(mute=False, reason=reason)
            await ctx.send(embed=create_embed(title="Unmuted", description=f"{member.mention} has been unmuted in the server."))
        except discord.Forbidden:
            await ctx.send(embed=create_embed(title="Error", description="I do not have permission to unmute members."))

def setup(bot):
    bot.add_cog(CommandsCog(bot))