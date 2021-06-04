import discord
import asyncio
import random
import datetime
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import increment
import asyncio
class Giveaway(commands.Cog):

  warning = "The user you are trying to {} is already a mod!"
  
  def __init__(self, bot):
    self.bot = bot

  @commands.command(brief="GiveAway Command")  
  @commands.has_permissions(kick_members=True)
  async def giveaway(self,ctx, duration: int, *, prize: str):
    if duration < 30:
      await ctx.send("Duration Has to Be greater Than 30 seconds")
    embed = discord.Embed(title=prize,
                          description=f"Hosted by - {ctx.author.name}\nReact with :tada: to enter!\nTime Remaining: **{duration}** seconds",
                          color=0xf1c40f)
    print("hi")
    msg = await ctx.channel.send(content=":tada: **GIVEAWAY** :tada:", embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(10)
    new_msg = await ctx.channel.fetch_message(msg.id)
    await asyncio.sleep(duration)
    user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != self.bot.user] 

    if len(user_list) == 0:
        await ctx.send("No one reacted.") 
    else:
        winner = random.choice(user_list)
        e = discord.Embed()
        e.title = "Giveaway ended!"
        e.description = f"You won: {prize}"
        e.timestamp = datetime.datetime.now()
        e.color = 0xf1c40f
        await ctx.send(f"{winner.mention}", embed=e)
def setup(bot):
  bot.add_cog(Giveaway(bot))
