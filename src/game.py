import discord
import asyncio
import toml
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tinydb import TinyDB, Query
from typing import Union
from tinydb.operations import *
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import re
import random
global counterr
counterr  = 1
Plot = Query()
User  = Query()
gb = TinyDB("./databases/game.toml")
cb = TinyDB('./databases/currency.toml')
plots = 5625
columns = 75 
global thatThingHappened  
rows = 75
directions = ['Right','Left','Down','Up']
global user_loc
user_loc = [0,0]
shop_dict = {
  1:"Vampire Plush -- 40 ClydeCoin",
  2: "Banshee Plush -- 40 ClydeCoin",
  3: "Zombie Plush -- 40 ClydeCoin",
  4: "Hydra Plush -- 40 ClydeCoin",
  5: "Chimera Plush -- 40 ClydeCoin",
  6: "Yeti Plush -- 40 ClydeCoin",
  7: "Dragon Plush -- 40 ClydeCoin",
  8: "Unicorn Plush -- 40 ClydeCoin",
  9: "Phoenix Plush -- 40 ClydeCoin",
  10: "Griffin Plush -- 40 ClydeCoin",
  11: "Clyde Plush -- 40 ClydeCoin",
  12: "Wumpus Plush -- 40 ClydeCoin",
  13: "Dog Plush -- 40 ClydeCoin",
  14: "Unicorn Plush -- 40 ClydeCoin",
  15: "Rock Emblem -- 10 ClydeCoin",
  16:"Iron Emblem -- 30 ClydeCoin",
  17: "Bronze Emblem -- 60 ClydeCoin",
  18: "Silver Emblem -- 140 ClydeCoin",
  19: "Gold Emblem -- 210 ClydeCoin",
  20: "Diamond Emblem -- 360 ClydeCoin",
  21:"Ruby Emblem -- 480 ClydeCoin",
  22:"ClydeStone Emblem -- 610 ClydeCoin",
  23:"Stick -- 3 ClydeCoin",
  24:"Small Rock -- 2 ClydeCoin",
  25:"Medium Rock -- 4 ClydeCoin",
  26:"Large Rock -- 8 ClydeCoin",
  27:"Boulder -- 22 ClydeCoin",
  28:"Log -- 10 ClydeCoin",
  28:"Yellow Flower -- 5 ClydeCoin",
  29:"Blue Flower -- 5 ClydeCoin",
  30:"Red Flower -- 5 ClydeCoin",
  31:"Bouquet -- 10 ClydeCoin",
  32:"Shovel -- 12 ClydeCoin",
  33: "Axe -- 15 ClydeCoin",
  34:"Sword -- 23 ClydeCoin",
  35:"Double-edged Sword -- 32 ClydeCoin",
  36:"Dagger -- 17 ClydeCoin",
  37:"Cursed Stone -- 20 ClydeCoin",
  38:"Mysterious Stone -- 20 ClydeCoin",
  39:"Relic of St. Clyde -- 12000 ClydeCoin",
  40:"Scroll -- 10 ClydeCoin",
  41:"Mint -- 1 ClydeCoin",
  42:"Leaf -- 1 ClydeCoin",
  43:"Bread -- 5 ClydeCoin",
  44:"Pie -- 7 ClydeCoin"
}
global ex
ex = len(shop_dict)
def append(field, n):
    """
    Append ``n`` to the Iterable in the given fields in the document.
    """
    def transform(doc):
        doc[field].append(n)

    return transform
class Game(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.thatThingHappened = False
    
  @commands.command()
  async def game(self, ctx):
   if isinstance(ctx.channel, discord.channel.DMChannel):
    await ctx.send("You Have Arrived At Spawn Area Owned By The Government. Use the Buttons Below to Go Right, Left, Up, Down")
    global user_location
    user_location =  []
    buttons_list = []
    for i in directions:
     buttons_list.append(Button(style=ButtonStyle.blue, label=f"{i}"))
    await ctx.send(
          f"‍‍⠀",
          components = [
            buttons_list
          ]
   
  
        )
  @commands.Cog.listener()   
  async def on_button_click(self, res):
   if isinstance(res.channel, discord.channel.DMChannel): 
    a = await res.channel.history(limit=3).flatten()
    def user_locupdate():
         
           if self.thatThingHappened == False:
              global user_loc
              user_loc = [0,0]
              self.thatThingHappened = True
             
           a = len(user_loc) 
           msg = ""
           msg2 =""
           if res.component.label == "Right":
              
                user_loc = [user_loc[0]+1,user_loc[1]]
                
           elif res.component.label == "Up":
             
               
              user_loc = [user_loc[0],user_loc[1]+1]
              print(user_loc)
              
              
           elif res.component.label == "Left":
               
                user_loc = [user_loc[0]-1,user_loc[1]]
               
                print(user_loc)
               
           elif res.component.label == "Down":

               user_loc = [user_loc[0],user_loc[1]-1]
              
               print(user_loc)
           
           if bool(gb.get(Plot.loc == user_loc)) == False:
              typ = "NONE"
              
              msg2 = "Plot Owned By Government"
           else:
             owner = gb.get(Plot.loc == user_loc)['owner']
             typ = gb.get(Plot.loc == user_loc)['type']
             msga2 = gb.get(Plot.loc == user_loc)['msg']
             if typ == "Private":
               msga2= 'This location is marked as strictly private, please do not enter.'
             elif typ == "Road":
               msga2 = "You are on a road."  
           
             msg2 = f"Plot Owner: {owner} Location: ({user_loc[0],user_loc[1]})\n {msga2}" 

            

           return msg2,user_loc,typ
           
    msg = ""
    msg,user_location,typ = user_locupdate()
    #user_locupdate()
    global counter
    counter = 1
    if counter == 1:
      if typ == "Store":
       owner = gb.get(Plot.loc == user_loc)['owner']
       em = discord.Embed(title=f":house_with_garden: **Item Store -- Run by {owner} **",description=f"Items--", color=0x7289da)
       for i in range(1,6):
         b = len(shop_dict)
         a = random.randint(1,b)
         em.add_field(name = f"**{i}**", value = f"**{shop_dict[a]}**")
       await res.respond(
         type=4,
         embed = em
        )  
      else:
        await res.respond(
         type=4,
         content  =  f"{msg}"
        )  
       
  @commands.command(brief = "Used to Claim a Plot And Set the type Of land")
  @commands.has_permissions(kick_members = True)
  async def claim(self,ctx,member:discord.Member = None,coordinates:commands.Greedy[int] = None,typ = None):
   
      if bool(gb.get(Plot.loc == coordinates)):
        await ctx.send("Plot already owned by a User, Use +own to transfer owners")   
      else:
        gb.insert({'loc':coordinates, 'owner':member.name,'type':typ,'msg':'Not Set By User','id':member.id})
        await ctx.send(f"Land Given To {member.name} having a type {typ}")   

  @commands.command(brief="Uset to Transfer ownership of a plot")
  @commands.has_permissions(kick_members = True) 
  async def own(slef,ctx, member:discord.Member = None, coordinates:commands.Greedy[int] = None, typ = None):
        if  bool(gb.get(Plot.loc == coordinates)) == False:
          await ctx.send("Plot Not Claimed By any User, use the +claim Command!")
        else:
          gb.update(set('owner',member.name),Plot.loc == coordinates)
          gb.update(set('type',typ),Plot.loc == coordinates)

          await ctx.send(f"Transferred Owner To {member.name}, set type to {typ}")

  @commands.command(brief = "To Set the Message To be Shown When User Lands Into You Plor")
  async def setMsg(self,ctx,coordinates:commands.Greedy[int] = None,*,msg = None):
     if isinstance(ctx.channel, discord.channel.DMChannel):
       print(coordinates)
       print(msg)
       if bool(gb.get(Plot.loc == coordinates)) == False:
          await ctx.send("*No one owns this property, however, so you can purchase it! Just open a ticket in our server.*")
       else:
         a = gb.get(Plot.loc == coordinates)['owner']
         if a == ctx.author.name:
           gb.update(set('msg',msg),Plot.loc == coordinates )  
           await ctx.send(f":white_check_mark: **The message was set for your land.***This is what people will see if they come across your land!*__Note: If you would like to make your property private or open a Store, please open a support ticket in our server.__")
         else:
           
           await ctx.send(f":no_entry_sign: **You don’t own this property.** *{a} owns this property. Contact them if you are interested in purchasing it.*")  
  @commands.command(brief = "Used To See Navigation Buttons Again")
  async def m(self,ctx):
   if isinstance(ctx.channel, discord.channel.DMChannel):
    buttons_list = []
    for i in directions:
     buttons_list.append(Button(style=ButtonStyle.blue, label=f"{i}"))
    await ctx.send(
          f"‍‍⠀",
          components = [
            buttons_list
          ]
    )  
  @commands.command(brief="Map For surrounding Plots")   
  async def map(self,ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
      user_loc_up = [user_loc[0],user_loc[1]+1]
      emoj = "<:green_square:847743058766331924>"
      typ = gb.get(Plot.loc == user_loc_up)['type']  
      if typ == "Private":
          emoj = "<:blue_square:847743058766331924>"
      elif typ == "Shop":
          print("ji")
          emoj = "<:red_square:847743058766331924>"
      elif typ == "Road":
          emoj = "<:brown_square:847743058766331924>"    
      user_loc_down = [user_loc[0],user_loc[1]-1]
      if bool(gb.get(Plot.loc == user_loc_down)):
        emoj1 = "<:green_square:847743058766331924>"
      else:
        typ = gb.get(Plot.loc == user_loc_down)['type']  
        if typ == "Private":
          emoj1 = "<:blue_square:847743058766331924>"
        elif typ == "Shop":
          emoj1 = "<:red_square:847743058766331924>"
        elif typ == "Road":
          emoj1 = "<:brown_square:847743058766331924>"
      if user_loc[0]  == 0:
        emoj2 = "<:green_square:847743058766331924>"
      ''' 
      user_loc_left = [user_loc[0]-1,user_loc[1]]
      emoj2 = "<:green_square:847743058766331924>"
      typ = gb.get(Plot.loc == user_loc_left)['type']  
      if typ == "Private":
          emoj2 = "<:blue_square:847743058766331924>"
      elif typ == "Shop":
          emoj2 = "<:red_square:847743058766331924>"
      elif typ == "Road":
          emoj2 = "<:brown_square:847743058766331924>"      
        '''        
      await ctx.send(f"⠀⠀{emoj}\n{emoj1}<:black_medium_square:785776583502856193><:green_square:847743058766331924>\n⠀⠀<:green_square:847743058766331924>")
      await ctx.send("Green:Government Owned Land, Blue:Private Land,Red: Shop, Brown:Road, Black: Current Location")

  @commands.command(brief="Buy From Plot Shop")
  async def buy(self,ctx,*,item = None):
   if not item:
     await ctx.send(":no_entry_sign: **Please enter the name of the item you would like to buy after the command.**\nExample: +buy Zombie Plush") 
   if isinstance(ctx.channel, discord.channel.DMChannel):
   
    for i in range(1,len(shop_dict)):
      if item in shop_dict[i]:
       global price
       cost = ""
       cost = ''.join(filter(lambda i: i.isdigit(), shop_dict[i]))
       print(cost)
       if cb.get(User.id == ctx.author.id)['coins'] >= int(cost):
        
        cb.update(append('items',item),User.id == ctx.author.id)
        await ctx.send(f":house_with_garden: **Item purchase complete! You now own {item}.**")
        cb.update(subtract('coins',int(cost)))
        owner = gb.get(Plot.loc == user_loc)['owner']
       
        cd.update(add('coins',25/100*int(cost)),User.id == "365974173803085826")
       else:
         await ctx.send("You Dont Have Enough Money") 
  @commands.command(brief="Edit Land Type")
  @commands.has_permissions(kick_members = True)
  async def EditLandType(self,ctx,coordinates: commands.Greedy[int] = None,typ = None):
    gb.update(set('type',typ),Plot.loc == coordinates)
    await ctx.send(f"Plot Set To Type {typ}")

  @commands.command(brief="View Inventory")
  async def viewInv(self,ctx):
     if isinstance(ctx.channel, discord.channel.DMChannel):
       embed = discord.Embed(title=f":shopping_bags: {ctx.author.name}\'s Inventory",description = "Items--")
       a = len(cb.get(User.id == ctx.author.id)['items'])
       for i in cb.get(User.id == ctx.author.id)['items']:
         counter = 1
         embed.add_field(name=f"**{counter}:**",value=f"**{i}**")
         counter+=1
       await ctx.send(embed = embed)

def setup(bot):
  bot.add_cog(Game(bot))    