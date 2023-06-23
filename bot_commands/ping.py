import discord
from discord.ext import commands


async def execute(message):
    await message.channel.send('pong')
        
        
        