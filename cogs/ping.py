import discord, math, os

from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

load_dotenv()

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping", description = "Check the status of the bot", guild_ids = list(map(int, os.getenv('GUILD_IDS').split(','))))
    async def _ping(self, ctx: SlashContext):
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {math.trunc(self.bot.latency*1000)} ms", color=0xff0000)
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Ping(bot))