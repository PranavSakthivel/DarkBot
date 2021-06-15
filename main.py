import discord, os

from discord.ext import commands
from dotenv import load_dotenv
from discord_slash import SlashCommand

load_dotenv()


bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

@bot.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(bot))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print("Cog Loaded: " + filename)

bot.run(os.getenv('DISCORD_TOKEN'))




