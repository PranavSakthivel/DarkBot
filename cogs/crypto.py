import discord, os, cryptocompare, ccy

from dotenv import load_dotenv
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

load_dotenv() # Guild IDs loaded from .env

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    coin_list = cryptocompare.get_coin_list(format=True) # Get list of all crypto coins from Cryptocompare API

    # Variables for easy use in command headers
    author_name = "Cryptocurrency"
    author_img = "https://i.imgur.com/a5rBAET.png"
    guild_list = list(map(int, os.getenv('GUILD_IDS').split(',')))

    # Helper method to verify if string can be converted to float safely
    # Credit: https://www.kite.com/python/answers/how-to-check-if-a-string-is-a-valid-float-in-python
    def check_float(self, potential_float):
        try:
            float(potential_float)
            return True
        except ValueError:
            return False

    @cog_ext.cog_slash(name="price", 
    description = "Check the current price of any crypto, in any currency", 
    guild_ids = guild_list,
    options=[
               create_option(
                    name="coin",
                    description="Which coin you want the price for",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="currency",
                    description="What to convert to (leave empty for USD)",
                    option_type=3,
                    required=False
                )
             ])
    async def _price(self, ctx: SlashContext, coin: str, convert_to: str = "USD"):
        # Handle lowercase input
        coin = coin.upper()
        convert_to = convert_to.upper()

        if not ccy.currency(convert_to): # Use currency module to check if currency code is valid
            embed = discord.Embed(title="Error", description=f"Currency \"{convert_to}\" does not exist", color=0xff0000)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

        elif coin not in self.coin_list: # Check coin list to make sure crypto exists
            embed = discord.Embed(title="Error", description=f"Crypto \"{coin}\" does not exist", color=0xff0000)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

        else:
            print(cryptocompare.get_price(coin, currency=convert_to, full=False)) # Get dictionary object of price
            embed = discord.Embed(title=f"{coin}", description=f"{str(cryptocompare.get_price(coin, currency=convert_to, full=False)[coin][convert_to])} {convert_to}", color=0xfcba03)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

    # Convert one crypto to another, or the other way around
    @cog_ext.cog_slash(name="convert", 
    description = "Convert cryptocurrency to fiat or vice versa", 
    guild_ids = guild_list,
    options=[
               create_option(
                    name="amount",
                    description="How much you want to convert",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="from",
                    description="What unit your current amount is in (Crypto code or currency code)",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="to",
                    description="Unit to convert to (Crypto code or currency code)",
                    option_type=3,
                    required=True
                )
             ])
    async def _convert(self, ctx: SlashContext, amount: str, from_unit: str, to_unit: str):
        # Check if amount string can be properly parsed into a float. TODO: Change when discord implements float checking
        if not self.check_float(amount) or float(amount) < 0: 
            embed = discord.Embed(title="Error", description="Amount must be a positive number", color=0xff0000)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

        # Check if both units exist in either the coin list or currency list
        elif from_unit not in self.coin_list and not ccy.currency(from_unit) or to_unit not in self.coin_list and not ccy.currency(to_unit):
            embed = discord.Embed(title="Error", description="Currency units are not valid", color=0xff0000)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

        else:
            result = 0
            if from_unit in self.coin_list: # Do crypto to fiat, then multiply
                result = round(float(amount) * cryptocompare.get_price(from_unit, currency=to_unit, full=False)[from_unit][to_unit], 2)
            else: # Do fiat to crypto, then divide
                result = round(float(amount) / cryptocompare.get_price(to_unit, currency=from_unit, full=False)[to_unit][from_unit], 2)

            embed = discord.Embed(title=f"{amount} {from_unit} to {to_unit}", description=f"{str(result)} {to_unit}", color=0xfcba03)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])
        
def setup(bot):
    bot.add_cog(Crypto(bot))