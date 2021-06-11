import discord
# import asyncio
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import *

User = Query()
xp = TinyDB('./databases/level.toml')
cb = TinyDB('./databases/currency.toml')
class Level(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.Cog.listener() 
  async def on_message(self,message):
    if bool(xp.get(message.author.id ==User.id)) == False:
      xp.insert({"id": message.author.id, "name": message.author.name, "xp": 0, "level": 1})

    xp.update(add("xp", 1), User.id == message.author.id)

    if xp.get(User.id == message.author.id)['xp'] >= xp.get(User.id ==  message.author.id)['level'] * 100 - xp.get(User.id ==         message.author.id)['level'] * 20:
     xp.update(add("level", 1), User.id == message.author.id) 
     level = cb.get(User.id == message.author.id)['level']
     await message.channel.send(f"**:+1: Congrats @{message.author.name}, You just leveled up to level {level}, :gift: *Enjoy your prize of :coin: 5 ClydeCoin!*")
     cb.update(add('coins', 5),User.id == message.author.id)

  @commands.command(brief="Check Your XP And Level Usage- +level @member")
  async def level(self, ctx, member:discord.Member = None) :
     if not member:
      if bool(xp.get(ctx.author.id == User.id)):
        em = discord.Embed(title=f"{ctx.author.name}\'s Level And Xp",description=f"**__XP__**\n {xp.get(ctx.author.id == User.id)['xp']}", color=0x7289da)
        em.add_field(name = "**__Level__**",value = xp.get(ctx.author.id == User.id)['level'])
        await ctx.send(embed = em)
      else:
        em = discord.Embed(title=f"{ctx.author.name}\'s Level And Xp",description=f"**__XP__** \n{xp.get(ctx.author.id == User.id)['xp']}", color=0x7289da)
        em.add_field(name = "**__Level__**",value = xp.get(ctx.author.id == User.id)['level'])
        await ctx.send(embed = em)
      
         
     else:
      if bool(cb.get(member.id == User.id)):
        em = discord.Embed(title=f"{member.name}\'s XP And Level ",description=f"**__XP__** is \n{xp.get(member.id == User.id)['xp']}", color=0x7289da)
        em.add_field(name = "**Level**",value = xp.get(member.id == User.id)['level'])
        await ctx.send(embed = em)
      else:
         em = discord.Embed(title=f"{ctx.author.name}\'s Level And Xp",description=f"**__XP__** \n{xp.get(ctx.author.id == User.id)['xp']}", color=0x7289da)
         em.add_field(name = "**__Level__**",value = xp.get(ctx.author.id == User.id)['level'])
         await ctx.send(embed = em)

      
 


def setup(bot):
  bot.add_cog(Level(bot))