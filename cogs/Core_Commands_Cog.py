import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction

class Core_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #group = app_commands.Group(name="parent", description="...")
    # Above, we declare a command Group, in discord terms this is a parent command
    # We define it within the class scope (not an instance scope) so we can use it as a decorator.

<<<<<<< HEAD
    #commands Command        
=======
    '''#commands Command        
>>>>>>> 950db3c0fb46fb67af4c62189b4c8ab56dd62d85
    @commands.hybrid_command(description = "View some helpful commands")
    async def command_list(self, ctx: discord.Interaction) -> None:
        embedVar = discord.Embed(description="Ask Sam for specifics", color=0xff0000)
        embedVar.add_field(name="Commands:", value="!ping" + '\n' + "!about")
<<<<<<< HEAD
        await ctx.send(embed=embedVar)
=======
        await ctx.send(embed=embedVar)'''
>>>>>>> 950db3c0fb46fb67af4c62189b4c8ab56dd62d85
        
    #About Command        
    @commands.hybrid_command(description = "About me for the bot")
    async def about(self, ctx: discord.Interaction) -> None:
        embedVar = discord.Embed(description="Sam's WIP bot. Recommend features please!",
                                 color=0x00ff00)
        await ctx.send(embed=embedVar)
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core_Commands(bot))

#groups = Core_Commands.group
        
        