import discord
from discord import app_commands
import typing
from discord.ext import commands, tasks
from discord import Interaction
import random
from discord.ui import Button, View


#League rank checker
from urllib.request import urlopen
from bs4 import BeautifulSoup 

#opening command
from cogs.music import music

#MAL search
from mal import *
#https://github.com/darenliang/mal-api/tree/master

import time

'''logger = settings.logging.getLogger("bot")'''

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    ''' #Roll Command        
    @commands.hybrid_command(description = "Prompt roll")
    async def roll(self, ctx: discord.Interaction, text):
        """Mudae helper"""
        await ctx.send('$' + text)'''

    #--------------------------------------------------------------------------
    
    #Slap Command        
    @commands.hybrid_command(description = "Slap someone :(")
    async def slap(self, ctx: discord.Interaction, user: discord.Member):
        """Get your anger across even if you aren't physically there"""
        await ctx.send('<@' + str(user.id) + '> was slapped!')
        
        
    #--------------------------------------------------------------------------
        
    #League rank check command        
    @commands.hybrid_command(description = "Expose someone's true elo")
    @app_commands.describe(username='Enter League of Legends username')
    async def league_rank(self, ctx: discord.Interaction, username: str):
        """Pull up the op.gg profile for a specified player"""
        urlName = username
        if ' ' in urlName: 
            urlName = urlName.replace(' ', "%20")
        url = "https://op.gg/summoners/na/" + urlName

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
        embedVar.set_thumbnail(url=league_pfp)
        await ctx.send(embed=embedVar)
        
        
    #--------------------------------------------------------------------------
        
    #Opening play request command        
    @commands.hybrid_command(description = "List the openings for desired anime")
    @app_commands.describe(anime='Anime to list the opening of')
    async def opening(self, ctx: discord.Interaction, anime: str) -> None:
        search = AnimeSearch(anime)
        
        url_split = search.results[0].url.split("/")
        anime_number = url_split[4]
        
        
        animePage = Anime(anime_number)
        
        await ctx.send(animePage.opening_themes)
        
        
        
    
    #--------------------------------------------------------------------------=     
    #MAL Search Command        
    @commands.hybrid_command(description = "Search an anime by name")
    @app_commands.describe(anime='Anime to search for')
    async def anime(self, ctx: discord.Interaction, anime: str) -> None:
        """Search an anime by name"""
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
    
    
    #--------------------------------------------------------------------------
    
    '''bomb_exploded = False
    first_click = False
    surrounding_bomb_count_arr = None
    totalArr = []
    revealedArr = []
    bomb_spots = []
    spots_cleared = 0
    @commands.hybrid_command(description = "Play a game of minesweeper")
    @app_commands.describe(number_bombs='Choose number of bombs to appear')
    async def minesweeper(self, ctx: discord.Interaction, number_bombs: str) -> None:
        """Play a game of minesweeper"""
        
        #loop through waiting for button clicks until a bomb is clicked
        async def minesweeper_button_click(interaction):
            i_val = int(int(interaction.data["custom_id"]) / 5)
            j_val = int(interaction.data["custom_id"]) % 5
            if Fun.first_click == False:
                surrounding_bomb_count_arr, bomb_spots = Fun.generate_bomb_board(Fun.totalArr, int(number_bombs), interaction.data["custom_id"])
                Fun.surrounding_bomb_count_arr = surrounding_bomb_count_arr
                Fun.bomb_spots = bomb_spots
                Fun.first_click = True
                Fun.revealedArr[i_val][j_val] = 1
            else:
                #update bombs
                clicked_bomb = False
                if int(interaction.data["custom_id"]) in Fun.bomb_spots:
                    clicked_bomb = True
                if clicked_bomb == True:
                    #LOST: CREATE EMBED WITH ALL BOMBS SHOWN AND RETURN
                    newView = View()
                    for num in range(25):
                        i_val = int(num/5)
                        j_val  = num % 5
                        if Fun.revealedArr[i_val][j_val] == 1:
                            button = Button(label = str(Fun.surrounding_bomb_count_arr[i_val][j_val]), custom_id = str(num), style = discord.ButtonStyle.blurple, disabled = True)
                            button.callback = minesweeper_button_click
                            newView.add_item(button)
                        elif num in Fun.bomb_spots:
                            if num == int(interaction.data["custom_id"]):
                                button = Button(label = "‎", emoji= "<:4493_Mushroom_Cloud:1134715685050794125>", custom_id = str(num), style = discord.ButtonStyle.blurple, disabled = True)
                                button.callback = minesweeper_button_click
                                newView.add_item(button)
                            else:
                                button = Button(label = "‎", emoji= "<:Bomb:1134713537030279258>", custom_id = str(num), style = discord.ButtonStyle.blurple, disabled = True)
                                button.callback = minesweeper_button_click
                                newView.add_item(button)

                        else:
                            button = Button(label = "?", custom_id = str(num), style = discord.ButtonStyle.blurple, disabled = True)
                            button.callback = minesweeper_button_click
                            newView.add_item(button)

                    newEmbed = discord.Embed(title = "Minesweeper Failed!")

                    newEmbed.add_field(name = "Total Bombs: " + str(number_bombs) + "        Spaces cleared: " + str(Fun.spots_cleared), value = "")
                    await interaction.response.edit_message(embed=newEmbed, view = newView)
                    return
   
            newView = View()
            for num in range(25):
                i_val = int(num/5)
                j_val  = num % 5
                if Fun.revealedArr[i_val][j_val] == 1:
                    button = Button(label = str(Fun.surrounding_bomb_count_arr[i_val][j_val]), custom_id = str(num), style = discord.ButtonStyle.blurple)
                    button.callback = minesweeper_button_click
                    newView.add_item(button)
                elif num == int(interaction.data["custom_id"]):
                    #TODO: ADD PROCESS OF FIGURING OUT IF BLANK INNER BLOCKS NEED TO BE REVEALED AS WELL
                    button = Button(label = str(Fun.surrounding_bomb_count_arr[i_val][j_val]), custom_id = str(num), style = discord.ButtonStyle.blurple)
                    button.callback = minesweeper_button_click
                    newView.add_item(button)
                    Fun.revealedArr[i_val][j_val] = 1
                    
                else:
                    button = Button(label = "?", custom_id = str(num), style = discord.ButtonStyle.blurple)
                    button.callback = minesweeper_button_click
                    newView.add_item(button)
            
            Fun.spots_cleared += 1
            newEmbed = discord.Embed(title = "Minesweeper")
                
            newEmbed.add_field(name = "Bombs left: " + str(number_bombs) + "        Spaces cleared: " + str(Fun.spots_cleared), value = "")
            await interaction.response.edit_message(embed=newEmbed, view = newView)
            return
    
        Fun.bomb_spots = []
        number_bombs = int(number_bombs)
        if not (number_bombs >= 1 and number_bombs <= 25):
            embedVar = discord.Embed(title = "Please enter a valid number of bombs")
            ctx.send(embedVar, ephemeral = True)
            return
            
            
        embedVar = discord.Embed(title = "Minesweeper")

        embedView = View()
        for i in range(25):
            button = Button(label = "?", custom_id = str(i), style = discord.ButtonStyle.blurple)
            button.callback = minesweeper_button_click
            embedView.add_item(button)
        
        
        embedVar.add_field(name = "Bombs left: " + str(number_bombs), value = "")
        embedVar.add_field
        await ctx.send(embed=embedVar, view = embedView)
        print("HERE")
        
        Fun.totalArr = []
        Fun.revealedArr = []
        for i in range(5):
            arr = []
            revealArr = []
            for j in range(5):
                arr.append(0)
                revealArr.append(0)
            Fun.totalArr.append(arr)
            Fun.revealedArr.append(revealArr)
        
        
        

        Fun.bomb_exploded = False
        Fun.first_click = False
        Fun.surrounding_bomb_count_arr = None
        Fun.spots_cleared = 0'''
        
        
        
                
      
    #--------------------------------------------------------------------------
    
    
    '''#modify array to initially have -1 if spot has a bomb, 0 if no bomb
    #then loop through again and calculate numbers for each spot
    def generate_bomb_board(arr, num_bombs, clicked_spot_val):
        #generate bomb spots
        bomb_spots = random.sample(range(0, 25), num_bombs)
        for val in range(len(bomb_spots)):
            #account for if generated bomb spot is where user first clicked
            if bomb_spots[val] == clicked_spot_val:
                new_bomb = random.randint(0, 25)
                while new_bomb in (item for sublist in bomb_spots for item in sublist):
                    new_bomb = random.randint(0, 25)
                bomb_spots[val] = new_bomb
        counter = 0
        for i in range(5):
            for j in range(5):
                if counter in bomb_spots and counter != clicked_spot_val:
                    arr[i][j] = -1
                else:
                    arr[i][j] = 0
                counter += 1
                
        #update spots with the correct number for surrouding bombs
        for i in range(5):
            for j in range(5):
                surrounding_bombs = 0
                if arr[i][j] != -1:
                    if i > 0:
                        #top left
                        if j > 0:
                            if arr[i-1][j-1] == -1:
                                surrounding_bombs += 1
                        #top middle
                        if arr[i-1][j] == -1:
                            surrounding_bombs += 1
                        #top right
                        if j < 4:
                            if arr[i-1][j+1] == -1:
                                surrounding_bombs += 1
                    #left
                    if j > 0:    
                        if arr[i][j-1] == -1:
                            surrounding_bombs += 1
                    #right
                    if j < 4:
                        if arr[i][j+1] == -1:
                            surrounding_bombs += 1
                    
                    if i < 4:
                        #bottom left
                            if j > 0:
                                if arr[i+1][j-1] == -1:
                                    surrounding_bombs += 1
                            #bottom middle
                            if arr[i+1][j] == -1:
                                surrounding_bombs += 1
                            #bottom right
                            if j < 4:
                                if arr[i+1][j+1] == -1:
                                    surrounding_bombs += 1
                
                arr[i][j] = surrounding_bombs
        return arr, bomb_spots'''
                
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))



