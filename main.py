import discord
import os
from discord.ext import commands
from tinydb import TinyDB, Query
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from quart import Quart
import os
app = Quart(__name__)

User = Query()
pre = TinyDB('./databases/prefix.toml')
intents = discord.Intents.all()
global bot
bot = commands.Bot(command_prefix = "+", case_insensitive = True, intents = intents)

@bot.event
async def on_ready():
  print("Ready!")
  await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = f"+help on {len(bot.guilds)} servers"))
  DiscordComponents(bot)


for file in os.listdir('./src'):
  if file.endswith(".py"):
    bot.load_extension(f"src.{file[:-3]}")
bot.loop.create_task(app.run_task('0.0.0.0', 8888))
bot.run("ODQ4NjE3MzI3MTA4NDIzNjkw.YLPOeQ.rHjIzE2Y7WydASKSJjDNVWAYQGA")
