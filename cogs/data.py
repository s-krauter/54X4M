import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
import sqlite3
from discord.ui import Button, View

#commands relating to SQL database
class databaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Jackbox funniness:
    #CREATE TABLE Jackbox(user_id, funniness, unfunniness, guild_id)
    '''Jackbox
        <int>User    <int>FunnyCount      <int>UnfunnyCount, Guild

    '''
    @commands.hybrid_command(description = "Acknowledge someone's funniness")
    async def funniness(self, ctx: discord.Interaction, user: discord.Member):
        con = sqlite3.connect('database.db')

        cur = con.cursor()

        response = cur.execute("SELECT user_id FROM Jackbox WHERE user_id = " + str(user.id) + " AND guild_id = " + str(ctx.guild.id))
        
        #if user does not have a value for current server, add one
        if response.fetchone() == None:
            cur.execute("INSERT INTO Jackbox(user_id, funniness, unfunniness, guild_id) VALUES (" + str(user.id) + ", 1, 0, " + str(ctx.guild.id) + ");")
            await ctx.send("User added to leaderboard. Funniness value now 1!")
            con.commit()
            return
        else:
            #do nothing
            funResponse = con.execute("SELECT funniness FROM Jackbox WHERE user_id = " + str(user.id) + " AND guild_id = " + str(ctx.guild.id))
            funInt = int(funResponse.fetchone()[0])
            funInt = funInt + 1
            funInt = str(funInt)
            cur.execute("UPDATE Jackbox SET funniness = " + funInt + " WHERE user_id = " + str(user.id) + " AND guild_id = " + str(ctx.guild.id))
            con.commit()
            await ctx.send(user.display_name + " has become funnier!")
            return
            
            
    #--------------------------------------------------------------------------

    @commands.hybrid_command(description = "View how funny (or not) members are!")
    @app_commands.choices(criteria=[
    app_commands.Choice(name='Funniness', value=1),
    app_commands.Choice(name='Unfunniness', value=2)
    ])
    async def clowns(self, ctx: discord.Interaction, criteria: app_commands.Choice[int]):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        
        testResponse = cur.execute("SELECT user_id FROM Jackbox WHERE guild_id = " + str(ctx.guild.id))
        if testResponse.fetchone()== None:
            await ctx.send("Sorry, no members have a silliness score!")
            return
        
        if criteria.name == "Funniness":
            response = cur.execute("SELECT user_id, funniness, unfunniness FROM Jackbox WHERE guild_id = " + str(ctx.guild.id) + " ORDER BY funniness DESC LIMIT 10")
        else:
            response = cur.execute("SELECT user_id, funniness, unfunniness FROM Jackbox WHERE guild_id = " + str(ctx.guild.id) + " ORDER BY unfunniness DESC LIMIT 10")
        userList = ""
        funList = ""
        unfunList = ""
        
        entryListings = response.fetchall()
        print(entryListings)
        ctr = 1
        for i in range(0, len(entryListings)):
            '''print((entryListings[i][0]))
            print(ctx.guild.get_member())'''
            userList += (str(ctr) + ". " + ctx.guild.get_member(int(entryListings[i][0])).display_name + '\n')
            funList += (str(entryListings[i][1]) + '\n')
            unfunList += (str(entryListings[i][2]) + '\n')
            ctr += 1
            print("ending loop")
        
        
        embedVar = discord.Embed(title = "Biggest Goofballs on the Server",
                                 color=0x00ff00)
        embedVar.add_field(name = "Users", value = userList)
        embedVar.add_field(name = "Silly Score", value = funList)
        embedVar.add_field(name = "Not silly number", value = unfunList)
        await ctx.send(embed=embedVar)
        
        
    #--------------------------------------------------------------------------

        
    #CREATE TABLE yo_mama(counter, guild_id)
    @commands.hybrid_command(description = "Add to yo mama counter or check how many have been made")
    @app_commands.choices(action=[
    app_commands.Choice(name='Increment', value=1),
    app_commands.Choice(name='Check Status', value=2)
    ])
    async def yo_mama(self, ctx: discord.Interaction, action: app_commands.Choice[int]):
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        
        if action.name == 'Increment':
            print("HERE")
            testResponse = cur.execute("SELECT counter FROM yo_mama WHERE guild_id = " + str(ctx.guild.id))
            if testResponse.fetchone() == None:
                cur.execute("INSERT INTO yo_mama(counter, guild_id) VALUES(1, " + str(ctx.guild.id) +")")
                con.commit()
                await ctx.send("yo mama counter incremented")
                return
        
            response = cur.execute("SELECT counter FROM yo_mama WHERE guild_id = " + str(ctx.guild.id))
            ctr = str(int(response.fetchone()[0]) + 1)
            
            cur.execute("UPDATE yo_mama SET counter = " + ctr + " WHERE guild_id = " + str(ctx.guild.id))
            
            cur.execute
            con.commit()
            await ctx.send("yo mama counter incremented")
            return

        else:
            print("HERE B")
            testResponse = cur.execute("SELECT counter FROM yo_mama WHERE guild_id = " + str(ctx.guild.id))
            if testResponse.fetchone() == None:
                await ctx.send("No yo mama jokes made")
                return
            
            response = cur.execute("SELECT counter FROM yo_mama WHERE guild_id = " + str(ctx.guild.id))
            ctr = str(response.fetchone()[0])
            
            embedVar = discord.Embed(title = "",
                                 color=0x00ff00)
        embedVar.add_field(name = "", value = "Server has suffered through ***" + ctr + "*** yo mama jokes")
        await ctx.send(embed=embedVar)
        
    #--------------------------------------------------------------------------

        
    correctAnswer = "a"
    correctButton = "A"
    @commands.hybrid_command(description = "Test your knowledge with some trivia")
    @app_commands.choices(category=[
    app_commands.Choice(name='animals', value=1),
    app_commands.Choice(name='brain-teasers', value=2),
    app_commands.Choice(name='celebrities', value=3),
    app_commands.Choice(name='entertainment', value=4),
    app_commands.Choice(name='for-kids', value=5),
    app_commands.Choice(name='general', value=6),
    app_commands.Choice(name='geography', value=7),
    app_commands.Choice(name='history', value=8),
    app_commands.Choice(name='hobbies', value=9),
    app_commands.Choice(name='humanities', value=10),
    app_commands.Choice(name='literature', value=11),
    app_commands.Choice(name='movies', value=12),
    #app_commands.Choice(name='music', value=13),
    app_commands.Choice(name='people', value=14),
    #app_commands.Choice(name='rated', value=15),
    app_commands.Choice(name='religion-faith', value=16),
    app_commands.Choice(name='science-technology', value=17),
    app_commands.Choice(name='sports', value=18),
    app_commands.Choice(name='television', value=19),
    app_commands.Choice(name='video-games', value=20)
    ])
    async def trivia(self, ctx: discord.Interaction, category: app_commands.Choice[int]):
        #CREATE TABLE trivia(Category, Question, Answer, OptionA, OptionB, OptionC, OptionD)
        #trivia questions ripped from https://github.com/uberspot/OpenTriviaQA/tree/master/categories
        
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        
        cat = category.name
        if cat == "brain-teaser":
            cat = "brain"
        if cat == "for-kids":
            cat = "kids"
        if cat == "video-games":
            cat = "games"
        if cat == "science-technology":
            cat = "science"
        if cat == "religion-faith":
            cat = "religion"
            
        response = cur.execute("SELECT Category, Question, Answer, OptionA, OptionB, OptionC, OptionD FROM trivia WHERE Category = '" + cat + "' ORDER BY RANDOM() LIMIT 1")
        
        answer = response.fetchall()
        
        
        
        buttonA = Button(label = "A", style = discord.ButtonStyle.blurple)
        buttonB = Button(label = "B", style = discord.ButtonStyle.blurple)
        buttonC = Button(label = "C", style = discord.ButtonStyle.blurple)
        buttonD = Button(label = "D", style = discord.ButtonStyle.blurple)
        embedView = View()
        embedView.add_item(buttonA)
        embedView.add_item(buttonB)
        embedView.add_item(buttonC)
        embedView.add_item(buttonD)
        
        databaseCommands.correctAnswer = answer[0][2]
        
        if answer[0][2] == answer[0][3]:
            databaseCommands.correctButton = buttonA
        if answer[0][2] == answer[0][4]:
            databaseCommands.correctButton = buttonB
        if answer[0][2] == answer[0][5]:
            databaseCommands.correctButton = buttonC
        if answer[0][2] == answer[0][6]:
            databaseCommands.correctButton = buttonD
        
        embedVar = discord.Embed(title = "Trivia! Category: " + category.name,
                                 color=0x00ff00)
        embedVar.add_field(name = "", value = answer[0][1] + '\n')
        if len(answer[0][5]) < 1:
            embedVar.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4])
        
        if len(answer[0][5]) >= 1 and len(answer[0][6]) >= 1:
            embedVar.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])
            
        if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
            embedVar.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])
        
        async def right_button_callback(interaction):
            newEmbed = discord.Embed(title = "Trivia! Category: " + category.name,
                                 color=0x00ff00)
            newEmbed.add_field(name= "Previous answer was correct!", value = "")
            
            response = cur.execute("SELECT Category, Question, Answer, OptionA, OptionB, OptionC, OptionD FROM trivia WHERE Category = '" + cat + "' ORDER BY RANDOM() LIMIT 1")
        
            answer = response.fetchall()
            
            databaseCommands.correctAnswer = answer[0][2]
            
            newEmbed.add_field(name = "", value = answer[0][1] + '\n')
            if len(answer[0][5]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) >= 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])
            
            if answer[0][2] == answer[0][3]:
                databaseCommands.correctButton = buttonA
            if answer[0][2] == answer[0][4]:
                databaseCommands.correctButton = buttonB
            if answer[0][2] == answer[0][5]:
                databaseCommands.correctButton = buttonC
            if answer[0][2] == answer[0][6]:
                databaseCommands.correctButton = buttonD
                
            if databaseCommands.correctButton == buttonA:
                buttonA.callback = right_button_callback
            else:
                buttonA.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonB:
                buttonB.callback = right_button_callback
            else:
                buttonB.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonC:
                buttonC.callback = right_button_callback
            else:
                buttonC.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonD:
                buttonD.callback = right_button_callback
            else:
                buttonD.callback = wrong_button_callback
            
            await interaction.response.edit_message(embed = newEmbed, view = embedView)
        
        async def wrong_button_callback(interaction):
            newEmbed = discord.Embed(title = "Trivia! Category: " + category.name,
                                 color=0x00ff00)
            newEmbed.add_field(name= "Incorrect. Previous answer was ", value = databaseCommands.correctAnswer)
            
            response = cur.execute("SELECT Category, Question, Answer, OptionA, OptionB, OptionC, OptionD FROM trivia WHERE Category = '" + cat + "' ORDER BY RANDOM() LIMIT 1")
        
            answer = response.fetchall()
            
            databaseCommands.correctAnswer = answer[0][2]
            
            newEmbed.add_field(name = "", value = answer[0][1] + '\n')
            if len(answer[0][5]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) >= 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])
            
            if answer[0][2] == answer[0][3]:
                databaseCommands.correctButton = buttonA
            if answer[0][2] == answer[0][4]:
                databaseCommands.correctButton = buttonB
            if answer[0][2] == answer[0][5]:
                databaseCommands.correctButton = buttonC
            if answer[0][2] == answer[0][6]:
                databaseCommands.correctButton = buttonD
                
            if databaseCommands.correctButton == buttonA:
                buttonA.callback = right_button_callback
            else:
                buttonA.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonB:
                buttonB.callback = right_button_callback
            else:
                buttonB.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonC:
                buttonC.callback = right_button_callback
            else:
                buttonC.callback = wrong_button_callback
            if databaseCommands.correctButton == buttonD:
                buttonD.callback = right_button_callback
            else:
                buttonD.callback = wrong_button_callback
            await interaction.response.edit_message(embed = newEmbed, view = embedView)
        
        if databaseCommands.correctButton == buttonA:
            buttonA.callback = right_button_callback
        else:
            buttonA.callback = wrong_button_callback
        if databaseCommands.correctButton == buttonB:
            buttonB.callback = right_button_callback
        else:
            buttonB.callback = wrong_button_callback
        if databaseCommands.correctButton == buttonC:
            buttonC.callback = right_button_callback
        else:
            buttonC.callback = wrong_button_callback
        if databaseCommands.correctButton == buttonD:
            buttonD.callback = right_button_callback
        else:
            buttonD.callback = wrong_button_callback
        
         
            
        await ctx.send(embed=embedVar, view = embedView)
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(databaseCommands(bot))




