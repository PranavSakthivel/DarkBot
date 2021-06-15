import discord
import os
import math

from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext

load_dotenv()

client = discord.Client(command_prefix="-", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))

@slash.slash(name="ping", description = "Check the status of the bot", guild_ids = [485523193952731156, 607020159336579083])
async def _ping(ctx: SlashContext):
    embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {math.trunc(client.latency*1000)} ms", color=0xff0000)
    await ctx.send(embeds=[embed])

client.run(os.getenv('DISCORD_TOKEN'))




