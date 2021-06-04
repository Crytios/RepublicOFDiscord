import discord
# import asyncio
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import *
from discord.ext.commands import BucketType, CommandOnCooldown, CommandNotFound, BadArgument
import random

User = Query()
cb = TinyDB('./databases/currency.toml')
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
class Currency(commands.Cog):

  def __init__(self, bot):
    self.bot = bot



  @commands.command(breif="Daily ClydeCoin")
  @commands.cooldown(1, 86400, BucketType.user)
  async def daily(self,ctx):
    if bool(cb.get(ctx.author.id == User.id)):
      val = random.randint(5,20)
      cb.update(add('coins',val), User.id == ctx.author.id)
      
      await ctx.send(f"**:gift: Congrats!, you just collected {val} ClydeCoin!**:crown: *Buy VIP to get another daily reward! Check it out in <#848980887865393252>*\n__Make sure to collect again in :alarm_clock: 24 hours!")
    else:
      cb.insert({'id':ctx.author.id, 'coins': 0,'items':[]})  
      val = random.randint(5,20)
      cb.update(add('coins',val),User.id == ctx.author.id)
      await ctx.send(f"**:gift: Congrats!, you just collected {val} ClyeCoin!**:crown: *Buy VIP to get another daily reward! Check it out in <#848980887865393252>*\n__Make sure to collect again in :alarm_clock: 24 hours!")


  @commands.command(brief="Daily Vip ClydeCoins") 
  @commands.cooldown(1, 86400, BucketType.user)
  async def vip(self,ctx):
    role1 = ctx.guild.get_roles(848929092731797514)
    role_names = [role.name for role in ctx.author.roles]

    if role1.name in role_names:

     if bool(cb.get(ctx.author.id == User.id)):
      val = random.randint(5,20)
      cb.update(add('coins',val), User.id == ctx.author.id)
      await ctx.send(f":crown: **Congrats!, you just collected {val} ClydeCoin using VIP!**\n__Make sure to collect again in :alarm_clock: 24 hours!__")
     else:
      cb.insert({'id':ctx.author.id, 'coins': 0,'items':[]})  
      val = random.randint(10,30)
      cb.update(add('coins',val),User.id == ctx.author.id)
      await ctx.send(f":crown: **Congrats!, you just collected {val} ClydeCoin using VIP!**\n__Make sure to collect again in :alarm_clock: 24 hours!__")
    else:
       await ctx.send(":no_entry_sign: **Sorry, you need to be a VIP subscriber to collect this bonus!**:crown: *Buy VIP to get this and many other rewards! Check it out in <#848980887865393252>*")  


  @commands.Cog.listener()   
  async def on_command_error(self,ctx, error):
    if  isinstance(error,CommandOnCooldown):
       em = discord.Embed(title=f"Slow  down ",description=f":no_entry_sign: **Sorry, you need to wait 24 Hours before collecting again!\n**:crown: *Buy VIP to get another daily reward! Check it out in <#848980887865393252>*", color=0x7289da)
       await ctx.send(embed=em)
      
  @commands.command(brief="Check Balance")
  async def bal(self,ctx,member:discord.Member = None):
    if not member:
     if bool(cb.get(ctx.author.id == User.id)):
      em = discord.Embed(title=f"{ctx.author.name}\'s Balance",
      description=f"** ClydeCoin Balance**:coin: {cb.get(ctx.author.id == User.id)['coins']} ClydeCoin \n__Buy more ClydeCoin in <#848921460093616138>" ,color=0x7289da)
      await ctx.send(embed = em)
     else:
        em = discord.Embed(title=f"{ctx.author.name}\'s Balance",description=f"**ClydeCoin Balance**:coin: {cb.get(ctx.author.id == User.id)['coins']} ClydeCoin \n__Buy more ClydeCoin in <#848921460093616138>", color=0x7289da)
        await ctx.send(embed = em)
         
    else:
      if bool(cb.get(member.id == User.id)):
        em = discord.Embed(title=f"{member.name}\'s Balance ",description=f"** ClydeCoin Balance**:coin: {cb.get(ctx.author.id == User.id)['coins']} ClydeCoin \n__Buy more ClydeCoin in <#848921460093616138>", color=0x7289da)
        await ctx.send(embed = em)
      else:
         em = discord.Embed(title=f"{member.name}\'s Balance",description=f"** ClydeCoin Balance**:coin: {cb.get(ctx.author.id == User.id)['coins']} ClydeCoin \n__Buy more ClydeCoin in <#848921460093616138>", color=0x7289da)
         await ctx.send(embed = em)

  @commands.command(brief="Add ClydeCouns")  
  @commands.has_permissions(kick_members=True)  
  async def addBal(self,ctx,bal: int = None,member:discord.Member=None):
    if bool(cb.get(ctx.author.id == User.id)) == False:
       cb.insert({'id':ctx.author.id, 'coins': 0,'items':''})  
    if not member:
      await ctx.send("Pls Specify Member")
    else:  
      cb.update(add('coins', int(bal)), User.id == member.id)
      await ctx.send(f"Added {bal} ClydeCoins to {member.name}")

  @commands.command(brief="Subtract ClydeCouns")  
  @commands.has_permissions(kick_members=True)  
  async def subBal(self,ctx,bal: int = None,member:discord.Member=None):
    if not member:
      await ctx.send("Pls Specify Member")
    else:
      cb.update(subtract('coins', int(bal)), User.id == member.id)
      await ctx.send(f"Subtracted {bal} ClydeCoins from {member.name}")
      
       
def setup(bot):
  bot.add_cog(Currency(bot))