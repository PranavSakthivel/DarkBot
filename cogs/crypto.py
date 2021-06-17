import discord, os, cryptocompare

from dotenv import load_dotenv
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

load_dotenv()

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    coin_list = cryptocompare.get_coin_list(format=True)
    author_name = "Cryptocurrency"
    author_img = "https://pixabay.com/get/g5bc01e0cade5809dda3b87b60087bed29820076c3b07fb15725f22f4335ec2ee2beefa45d87627f66c8bdb647c7ede1b_640.png"
    guild_list = list(map(int, os.getenv('GUILD_IDS').split(',')))

    @cog_ext.cog_slash(name="price", 
    description = "Check the current price of any crypto, in any currency (default: USD)", 
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
                    description="What to convert to",
                    option_type=3,
                    required=False
                )
             ])
    async def _price(self, ctx: SlashContext, coin: str, convert_to: str = "USD"):
        coin.upper()
        if coin not in self.coin_list: # TODO: More error handling
            await ctx.send(embeds=[discord.Embed(title=f"Type \"{coin}\" does not exist", description="Please use `/list` to view a list of valid currencies.", color=0xff0000)])
        else:
            embed = discord.Embed(title=f"{coin}", description=f"{str(cryptocompare.get_price(coin, currency=convert_to, full=False)[coin][convert_to])} {convert_to}", color=0xfcba03)
            embed.set_author(name=self.author_name, icon_url=self.author_img)
            await ctx.send(embeds=[embed])

    # @cog_ext.cog_slash(name="list", 
    # description = "List all available coin/currencies", 
    # guild_ids = guild_list)
    # async def _list(self, ctx: SlashContext):
    #     await ctx.author.create_dm()
    #     await ctx.author.send(str(self.coin_list))
    #     await ctx.send("DM sent!")
        
def setup(bot):
    bot.add_cog(Crypto(bot))