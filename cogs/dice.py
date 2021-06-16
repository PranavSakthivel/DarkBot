import discord, os, random

from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

load_dotenv()

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="dice", 
    description = "Roll some dice!", 
    guild_ids = list(map(int, os.getenv('GUILD_IDS').split(','))),
    options=[
               create_option(
                 name="sides",
                 description="Number of sides per die",
                 option_type=4,
                 required=True
               ),
               create_option(
                 name="number",
                 description="Number of dice to roll. If left empty, will roll 1 die",
                 option_type=4,
                 required=False
               ),
               create_option(
                 name="modifier",
                 description="Modifier: ",
                 option_type=4,
                 required=False
               )
             ])
    async def _dice(self, ctx: SlashContext, sides: int, number: int = 1, modifier: int = 0):
        if (number < 1 or sides < 1):
            embed = discord.Embed(title = "Error", description = "You can't roll negative dice!", color=0xff0000)
            embed.set_author(name="Dice", icon_url="https://i.imgur.com/G164YiZ.png")

            await ctx.send(embeds=[embed])

        elif (sides > 120):
            embed = discord.Embed(title = "Error", description = "You can't have a die with more than 120 sides!", color=0xff0000)
            embed.set_author(name="Dice", icon_url="https://i.imgur.com/G164YiZ.png")

            await ctx.send(embeds=[embed])

        elif (number > 200):
            embed = discord.Embed(title = "Error", description = "Are you really trying to roll more than 200 dice?", color=0xff0000)
            embed.set_author(name="Dice", icon_url="https://i.imgur.com/G164YiZ.png")

            await ctx.send(embeds=[embed])

        elif (modifier > 10000):
            embed = discord.Embed(title = "Error", description = "A modifier above 10,000? Really?", color=0xff0000)
            embed.set_author(name="Dice", icon_url="https://i.imgur.com/G164YiZ.png")

            await ctx.send(embeds=[embed])

        else:
            diceStr = ""
            result = 0
            
            for _ in range(number):
                roll = random.randint(1, sides)
                diceStr += "[" + str(roll) + "] "
                result += roll

            result += modifier

            footer = f"{number} {sides}-sided dice"
            if (modifier > 0):
                diceStr += f" + {modifier}"
                footer += f", with modifier {modifier}"

            embed = discord.Embed(title = f"**{result}**", description=f"{diceStr}", color=0x22a7cc)
            embed.set_author(name="Dice", icon_url="https://i.imgur.com/G164YiZ.png")
            embed.set_footer(text=footer)

            await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Dice(bot))