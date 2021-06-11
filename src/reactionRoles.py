import discord
import numpy as np
from discord.utils import get
from typing import Final
import asyncio
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import *
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

Server = Query()
rr = TinyDB("./databases/rr.toml")

class Reaction(commands.Cog):
  global roles  
  roles = []
  
  def __init__(self, bot):
    self.bot = bot
  def randomCol(arr):
    return np.random.choices(arr)
  @commands.command(brief="Used to Set Up ReactionRoles Usage- +setreactionroles <roleid>")  
  @commands.has_permissions(manage_roles = True)
  async def setreactionroles(self, ctx, roleid=None):
          roles.append(roleid)
          await ctx.send("Added Role")
          global roles1
          roles1 = tuple(roles)
          print(roles1)

  @commands.command(brief="Used to Send the Reaction Roles Message Usage- +ReactionRoles")
  @commands.has_permissions(manage_roles = True)
  async def ReactionRoles(self,ctx):
      colors = ['blue','red','green','grey','gray']
      print(roles1)
     
      buttons_list = []
      for rolesa in roles1:
        role = get(ctx.guild.roles, id = int(rolesa))
        counter = 1
        buttons_list.append(Button(style=ButtonStyle.gray, label=role.name))
        
        #a:Final = len(role.name)
        #if len(role.name) < a:
         # b = a-len(role.name)
         # for i in range(b):
          #  q +="⠀"
       # else:
        #  b = 0 
         # q = ""
      await ctx.send(
          f"‍‍⠀",
          components = [
            buttons_list
          ]
        )
      counter+=1
      
      
    
  @commands.Cog.listener()   
  async def on_button_click(self, res):
   
    await res.respond(
         type=6,
         content = f" {await res.guild.get_member(res.user.id).add_roles(get(res.guild.roles, name=f'{res.component.label}'))}"
        ) 
        

  @commands.command(brief="Used to Set the Role The User gets joining the server Usage- +setjoinrole <roleid>")
  @commands.has_permissions(manage_roles = True)
  async def setjoinrole(self,ctx,role=None):
    if not role:
      await ctx.send("Pls specify Role ID")

    else:
      if bool(rr.get(ctx.guild.id == Server.id)):
        await ctx.send("You already Have set A Role for this Server!")
        await ctx.send("Reset Role to specified Role ID?Answer With Yes/No")   
        msg = await self.bot.wait_for('message', check = "Yes") 
        
        if msg:
          if msg.author == ctx.author:
            rr.update(set(roleid,role),Server.id == ctx.guild.id)
            await ctx.send("Role Updated")
      
          
      else:
        rr.insert({'id': ctx.guild.id, 'roleid': role})  
        await ctx.send("Role Set")

  @commands.Cog.listener()   
  async def on_member_join(member):
    guild_id = member.guild.id

    if bool(rr.get(guild_id == Server.id)):
     role_id = rr.get(guild_id == Server.id)['roleid']
     guild = self.bot.get_guild(guild_id)
     role = get(guild.roles, id=f'{role_id}')
     await member.add_roles(role)
     

def setup(bot):
  bot.add_cog(Reaction(bot))

