import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
import datetime, time

class Core_Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core_Commands(bot))

#groups = Core_Commands.group
        
        