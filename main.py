import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import sys

from cogs.Core_Commands_Cog import Core_Commands
from cogs.tests import Fun

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
            
#Ping Command        
@bot.tree.command(name = "ping", description = "Ping the bot and get response time.")
async def ping(interaction) -> None:
     await interaction.response.send_message(f'Ponggers! {round(bot.latency * 1000)}ms response time')

  
#bot online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.add_cog(Core_Commands(bot))
    await bot.add_cog(Fun(bot))
    #await bot.load_extension(cogs.tester)
    #load cogs
    '''for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')'''
     
     
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

bot.activity = discord.Game(name='/about')

#log in to bot with token
bot.run('MTA1NTIxOTYyMzQyOTE0ODgwMg.G7HXH6.m8j0uh_KaCWSkepTAiDHY6qwbDmXwt0EATP80U')

'''client = discord.Client(activity=discord.Game(name='my game'))

# or, for watching:
activity = discord.Activity(name='my activity', type=discord.ActivityType.watching)
client = discord.Client(activity=activity)'''



