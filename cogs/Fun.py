import discord
from discord import app_commands
import typing
from discord.ext import commands
from discord import Interaction


#League rank checker
from urllib.request import urlopen
from bs4 import BeautifulSoup 

#MAL search
from mal import *
#https://github.com/darenliang/mal-api/tree/master

import time

'''logger = settings.logging.getLogger("bot")'''

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    #--------------------------------------------------------------------------
    
    #Slap Command        
    @commands.hybrid_command(description = "Slap someone :(")
    async def slap(self, ctx: discord.Interaction, user: discord.Member):
        await ctx.send('<@' + str(user.id) + '> was slapped!')
        
        
    #--------------------------------------------------------------------------
        
    #League rank check command        
    @commands.hybrid_command(description = "Expose someone's true elo")
    async def league_rank(self, ctx: discord.Interaction, username: str):
        url = "https://op.gg/summoners/na/" + username

        # We use try-except incase the request was unsuccessful because of 
        # wrong URL
        try:
            page = urlopen(url)
        except:
            print("There is no account of this name or the summoner is unranked")
   
        soup = BeautifulSoup(page, 'html.parser')

        content = soup.find('meta', {"name":"description"})
        content = str(content)
        valList = content.split("/")
        
        if "LP" not in valList[1]:
            embedVar = discord.Embed(title="")
            embedVar.add_field(name="", value="Invalid user or user does not have a rank.")
            await ctx.send(embed=embedVar)

        #split up string to get record
        recordStr = valList[2].split(" ")

        #split up string of champs played to grab most played champ
        mostPlayedStr = valList[3].split(",")

        #split up Champ by name, then win rate
        champSplit = mostPlayedStr[0].split("-")
        mostPlayedChampName = champSplit[0]
        mostPlayedChampRecord = champSplit[1].split(" ")
        
        #find league pfp to add to embed
        contentB = soup.find('div', {"class": "profile-icon"})
        contentB = str(contentB)
        trimBeforeURL = contentB.split("src=")
        trimAfterURL = trimBeforeURL[1].split("/><")
        league_pfp = trimAfterURL[0][1:-1]


        embedVar = discord.Embed(color = discord.Color.dark_teal(), title=username + "'" + 's Ranked Statistics')
        embedVar.add_field(name="", value= username + " is" + valList[1] + "with a " + valList[2][-4:] + "win rate." + '\n' + 
                           "Overall Record: " + recordStr[1][0:-2] + " - " + recordStr[2][0:-3] + '\n' +
                           "Most played champion:" + mostPlayedChampName + " with a record of " + mostPlayedChampRecord[1][0:-2] + " - " + mostPlayedChampRecord[2][0:-3] + " (" + mostPlayedChampRecord[5] + " WR)")
        '''embedVar.add_field(name="Overall Record", value= recordStr[1][0:-2] + " - " + recordStr[2][0:-3] + '                                            ')
        embedVar.add_field(name="Favorite Champion", value= "Most played champion:" + mostPlayedChampName + " with a record of " + mostPlayedChampRecord[1][0:-2] + " - " + mostPlayedChampRecord[2][0:-3] + " (" + mostPlayedChampRecord[5] + " WR)")'''       
        embedVar.set_thumbnail(url=league_pfp)
        await ctx.send(embed=embedVar)
        
        
    #--------------------------------------------------------------------------
        
    
        
    
    #--------------------------------------------------------------------------
        
    #MAL Search Command        
    @commands.hybrid_command(description = "Search an anime by name")
    async def anime(self, ctx: discord.Interaction, anime: str) -> None:
        search = AnimeSearch(anime)
        
        url_split = search.results[0].url.split("/")
        anime_number = url_split[4]
        
        
        animePage = Anime(anime_number)
        embed_genres = str(animePage.genres)[1:-1]
        
        studio = str(animePage.studios)
        studio = studio.replace("[", "")
        studio = studio.replace("]", "")
        studio = studio.replace("'", "")
        
        embedVar = discord.Embed(title = search.results[0].title, url=search.results[0].url,
                                 color=0x00ff00)
        
        embedVar.add_field(name = "", value = "Score: " + str(search.results[0].score) + '\n' + "Rank #" + str(animePage.rank) + ", Popularity #" + str(animePage.popularity) + '\n' + str(animePage.type) + '\n' + str(search.results[0].episodes) + " episode(s), " + animePage.duration + '\n' + "Genres: " + embed_genres + '\n' + studio + '\n' + search.results[0].synopsis)
        embedVar.set_thumbnail(url=search.results[0].image_url)
        await ctx.send(embed=embedVar)
        
    
    #--------------------------------------------------------------------------
    
    
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))



