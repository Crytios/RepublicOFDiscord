import discord
# import asyncio
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import increment
import asyncio
Word = Query()
User = Query()
wx = TinyDB('./databases/warn.toml')
global bl_words
bl_words = []
class Moderation(commands.Cog):

  warning = "The user you are trying to {} is already a mod!"
  
  def __init__(self, bot):
    self.bot = bot
  @commands.command(brief="Set Blacklist Words")
  @commands.has_permissions(kick_members=True)
  async def setblword(self,ctx, word = None):
   if not word:
     await ctx.send("Specify Word")
   else:
      a = len(bl_words)
      if a > 0:
       for x in bl_words:
        if word == x:
         await ctx.send("Word already Added")
        else:
         bl_words.append(word)
         await ctx.send("Added")
      else:
         bl_words.append(word)
         await ctx.send("Added")

  @commands.command(brief = "Used to kick members out of a server")
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member = None, *, reason = "Not Specified"):

        if not member:
              await ctx.send("Command Usage: `+kick <member> <reason (optional)>`")

        else:
              embed = discord.Embed(
                color = discord.Color.red(),
              )

              embed.set_author(name = f"[KICKED] {member.name}", icon_url = member.avatar_url)

              embed.add_field(name = "Member", value = member.name)
              embed.add_field(name = "Moderator", value = ctx.author.name)
              embed.add_field(name = "Reason", value = reason)

              embed.set_footer(text = "Kick Command")

              await ctx.send(embed = embed)
              
              await member.kick()  

  @commands.command(brief = "Used to ban members from of a server")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member = None, reason = "Not Specified"):


     

    if not member:
      await ctx.send("Command Usage: `+ban <member> <reason (optional)>`")

    else:
        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"[BANNED] {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "Ban Command")

        await ctx.send(embed = embed)

        
        await member.ban()  

  @commands.command(brief = "Used to kick members out of a server")
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, member, *, reason = "Not Specified"):
    banned_users = await ctx.guild.bans()
    member_name,member_discrim = member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user

      if(user.name, user.discriminator) == (member_name, member_discrim):
        await ctx.guild.unban(user)
        embed = discord.Embed(
          color = discord.Color.green(),
        )

        embed.set_author(name = f"[UNBANNED] {user.name}", icon_url = user.avatar_url)

        embed.add_field(name = "Member", value = user.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "Ban Command")

        await ctx.send(embed = embed)

      
  @commands.command(brief = "Used to mute people from a server")
  @commands.has_permissions(manage_roles=True)
  async def mute(self, ctx, member: discord.Member = None, reason = "Not Specified"):

   
    if not member:
      await ctx.send("Command Usage: `+mute <member> <reason (optional)>`")

    else:
      arr = [role.name for role in ctx.channel.guild.roles if role.name == "Muted"]
      
      if bool(arr) == False:

        await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False))
        for role in ctx.channel.guild.roles:
         if role.name == str("Muted"):
          await member.add_roles(role)

        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"[MUTED] {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "Mute Command")

        await ctx.send(embed = embed)

      else:
        for role in ctx.channel.guild.roles:
         if role.name == str("Muted"):
          await member.add_roles(role)

        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"MUTED {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "Mute Command")

        await ctx.send(embed = embed)      
  @commands.command(brief = "Used to unmute people from a server")
  @commands.has_permissions(manage_roles=True)
  async def unmute(self, ctx, member: discord.Member = None, reason = "Not Specified"):

   
    if not member:
      await ctx.send("Command Usage: `+mute <member> <reason (optional)>`")

    else:
      arr = [role.name for role in ctx.channel.guild.roles if role.name == "Muted"]
      
      if bool(arr) == False:

        await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False))
        for role in ctx.channel.guild.roles:
         if role.name == str("Muted"):
          await member.remove_roles(role)

        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"[UNMUTED] {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "UnMute Command")

        await ctx.send(embed = embed)

      else:
        for role in ctx.channel.guild.roles:
         if role.name == str("Muted"):
          await member.remove_roles(role)

        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"UNMUTED {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = "UnMute Command")

        await ctx.send(embed = embed)      
  
  @commands.command(brief = "Used to warn people in a server")
  @commands.has_permissions(administrator=True)
  async def warn(self, ctx, member: discord.Member = None, reason = "Not Specified"):
    if bool(wx.get(member.id == User.id)):
        warn_counter = wx.get(member.id==User.id)['counter'] 
        wx.update(increment('counter'), User.id == member.id)
        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"Warned {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = f"This is The users {warn_counter} warn")

        await ctx.send(embed = embed) 
        channel = await member.create_dm()
        await channel.send(f"You Have Been Warned In The Server The Republic Of Discord for reason:{reason}")

        if warn_counter >=5:
          await member.ban()

    else:
        wx.insert({'id':member.id, 'counter':1})     
        warn_counter = wx.get(member.id==User.id)['counter'] 
        wx.update(increment('counter'), User.id == member.id)
        embed = discord.Embed(
          color = discord.Color.red(),
        )

        embed.set_author(name = f"Warned {member.name}", icon_url = member.avatar_url)

        embed.add_field(name = "Member", value = member.name)
        embed.add_field(name = "Moderator", value = ctx.author.name)
        embed.add_field(name = "Reason", value = reason)

        embed.set_footer(text = f" This is  user has {warn_counter} warns")

        await ctx.send(embed = embed) 

        if warn_counter >=10:
          await member.ban()
  @commands.command(brief="Send A message to everyone in a server")
  @commands.has_permissions(kick_members = True)
  async def send(self,ctx,*,msg = None):
    if not msg:
      await ctx.send("Specify Message")
    else:
      for i in ctx.guild.members:
        embed = discord.Embed(title=":bellhop: **Official Community Announcement**",description=f"**{msg}\n By-{ctx.author.name}**",color= discord.Color.red())
        await i.send(embed = embed)  
        await ctx.sent("Message Sent!")
  @commands.Cog.listener()
  async def on_message(self,message):
   f = "setblword"
   if not f in message.content:
    for w in bl_words:
      if w in message.content:
        
        await message.channel.send("<:no_entry_sign:785776583502856193> Message removed due to profanity. ")
        await asyncio.sleep(3)
        await message.channel.purge(limit = 2)
def setup(bot):
  bot.add_cog(Moderation(bot))
