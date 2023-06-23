import discord
from discord.ext import commands
import sys
sys.path.append('C:\CodingProjects\DiscBot\bot_commands')
import bot_commands
from bot_commands import ping, about

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

commands.command()
async def ping(ctx, description = "You are the best"):
    await ctx.channel.send('pong!!')

async def isValidCommand(message):
    '''if message.content == '!ping':
        await ping.execute(message)'''
        
    if message.content == '!about':
        await about.execute(message)
        