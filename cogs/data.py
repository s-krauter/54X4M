import discord
from discord import app_commands
from discord.ext import commands
from discord import Interaction
import sqlite3
from discord.ui import Button, View
import requests
import urllib.request
from PIL import Image
import math
from easy_pil import Canvas, Editor, Font
import calendar
from datetime import datetime
import pickle

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
    @app_commands.describe(criteria='Which criteria to order the leaderboard by')
    async def clowns(self, ctx: discord.Interaction, criteria: app_commands.Choice[int]):
        """List the (un)funniest people in the server"""
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
        
        ctr = 1
        for i in range(0, len(entryListings)):

            member = ctx.guild.get_member(int(entryListings[i][0]))
            if member != None:
                userList += (str(ctr) + ". " + ctx.guild.get_member(int(entryListings[i][0])).display_name + '\n')
                funList += (str(entryListings[i][1]) + '\n')
                unfunList += (str(entryListings[i][2]) + '\n')
                ctr += 1

        
        if criteria.name == "Funniness":
            embedVar = discord.Embed(title = "Biggest Goofballs on the Server " + "<a:5605ronaldo:1134726145552687194>",
                                     color=0x00ff00)
            embedVar.add_field(name = "Users", value = userList)
            embedVar.add_field(name = "Silly Score", value = funList)
            embedVar.add_field(name = "Not silly number", value = unfunList)
            await ctx.send(embed=embedVar)
        else: 
            embedVar = discord.Embed(title = "Least funny people on the Server " + "<:1706brage:1134726157133164565>",
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
        embedVar.add_field(name = "", value = "Server has enjoyed through ***" + ctr + "*** yo mama jokes " + "<a:5605ronaldo:1134726145552687194>")
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
    @app_commands.describe(category='Choose a category to be quizzed on')
    async def trivia(self, ctx: discord.Interaction, category: app_commands.Choice[int]):
        """Play some trivia"""
        #CREATE TABLE trivia(Category, Question, Answer, OptionA, OptionB, OptionC, OptionD)
        #trivia questions ripped from https://github.com/uberspot/OpenTriviaQA/tree/master/categories
        
        con = sqlite3.connect('database.db')

        cur = con.cursor()
        
        cat = category.name
        if cat == "brain-teasers":
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
            embedVar.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])
            
        if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
            embedVar.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])
        
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
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])
            
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
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5] + '\n' + "D: " + answer[0][6])

            if len(answer[0][5]) >= 1 and len(answer[0][6]) < 1:
                newEmbed.add_field(name = "", value = "A: " + answer[0][3] + '\n' + "B: " + answer[0][4] + '\n' + "C: " + answer[0][5])
            
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
    
    #--------------------------------------------------------------------------
    
    @commands.hybrid_command(description = "View a user's avatar history")
    async def avatar_history(self, ctx: discord.Interaction, user: discord.Member):

        #https://stackoverflow.com/questions/72723928/how-to-combine-several-images-to-one-image-in-a-grid-structure-in-python
        def combine_images(columns, space, images):
            rows = len(images) // columns
            if len(images) % columns:
                rows += 1
            width_max = 300
            height_max = 300
            background_width = width_max*columns# + (space*columns)-space
            background_height = height_max*rows# + (space*rows)-space
            background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
            x = 0
            y = 0
            for i, image in enumerate(images):
                img = Image.open(image)
                img = img.resize((300, 300))
                background.paste(img, (x, y))
                x += width_max# + space
                if (i+1) % columns == 0:
                    y += height_max# + space
                    x = 0
            background.save('C:/CodingProjects/DiscBot/avatars/avatarGroupImage.png')
        
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        response = cur.execute("SELECT avatar_num FROM avatars WHERE user_id = ? and guild_id = ? ORDER BY avatar_num DESC", (user.id, ctx.guild.id))
        res = response.fetchone()
        
        imgArr = []
        
        for i in range(1, res[0] + 1):
            imgStr = "C:/CodingProjects/DiscBot/avatars/" + str(user.id) + str(ctx.guild.id) + str(i) + ".png"
            imgArr.append(imgStr)
        
        arrCount = int(math.sqrt(res[0]))

        
        combine_images(arrCount, 20, imgArr)
        
        embedVar = discord.Embed(title = user.display_name + "'s avatar history on the server")
        
        avatarImg = discord.File("C:/CodingProjects/DiscBot/avatars/avatarGroupImage.png", filename = "image.png")
        embedVar.set_image(url="attachment://image.png")
        await ctx.send(embed=embedVar, file = avatarImg)
               
    #--------------------------------------------------------------------------

    #cur.execute("CREATE TABLE avatars(user_id, guild_id, avatar_num, avatar_url)")
    
    def update_avatars(member_id, guild_id, avatar_url):
        con = sqlite3.connect('database.db')

        cur = con.cursor()

        response = cur.execute("SELECT avatar_num, avatar_url FROM avatars WHERE user_id = {member} AND guild_id = {guild_id} ORDER BY avatar_num DESC".format(member = member_id, guild_id = guild_id))
        
        queryList = response.fetchone()
        if queryList == None:
            #insert into database
            cur.execute('''INSERT INTO avatars VALUES(?, ?, ?, ?)''', (member_id, guild_id, 1, avatar_url))
            con.commit()
            
            #save to avatars folder
            fileName = str(member_id) + str(guild_id) + str(avatar_url) + ".png"
            dest = "C:/CodingProjects/DiscBot/avatars/"
            img = requests.get(avatar_url).content
            with open('C:/CodingProjects/DiscBot/avatars/' + str(member_id) + str(guild_id) + "1" + ".png", 'wb') as handler:
                handler.write(img)
                handler.close()
            
            return
        else:
            #add current avater
            if queryList[1] != avatar_url:
                #insert into database
                idx = queryList[0] + 1
                cur.execute('''INSERT INTO avatars VALUES(?, ?, ?, ?)''', (member_id, guild_id, idx, avatar_url))
                con.commit()
                
                #save to avatars folder
                #save to avatars folder
                fileName = str(member_id) + str(guild_id) + str(avatar_url) + ".png"
                dest = "C:/CodingProjects/DiscBot/avatars/"
                img = requests.get(avatar_url).content
                with open('C:/CodingProjects/DiscBot/avatars/' + str(member_id) + str(guild_id) + str(idx) + ".png", 'wb') as handler:
                    handler.write(img)
                    handler.close()
                
    


    
    
    def create_user_todo(user_id, user_name):
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)
        
        userData = ToDo()
        userData.leftHeader = user_name + "'s To-Do List"
        
        todoDatas[user_id] = userData
        
        with open("todoDatas.pkl", 'wb') as fp:
            pickle.dump(todoDatas, fp)
        
        
        
        
        
        
    
    #CREATE TABLE todo(user, userData)
    @commands.hybrid_command(description = "Update/Customize your ToDo List")
    @app_commands.choices(field=[
    app_commands.Choice(name = 'textcolor', value = 1),
    app_commands.Choice(name = 'background', value = 2),
    app_commands.Choice(name = 'Left Header', value = 3),
    app_commands.Choice(name = 'Right Header', value = 4),
    ])
    async def update_todo(self, ctx: commands.Context, field: app_commands.Choice[int], updated_value: str):
        user_id = ctx.author.id
        user_name = ctx.author.name
        
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)
        
        
        if user_id not in todoDatas:
            databaseCommands.create_user_todo(user_id, user_name)
            
        userData = todoDatas[user_id]
         
        cat = field.name
        if cat == "textcolor":
            userData.textColor = updated_value
        elif cat == "background":
            #todo: download image and set it as their new one, make sure to crop it to correct size
            #download image and write to folder
            userData.background = updated_value
        elif cat == "Left Header":
            userData.leftHeader = updated_value
        elif cat == "Right Header":
            userData.rightHeader = updated_value

        with open("todoDatas.pkl", 'wb') as fp:
            pickle.dump(todoDatas, fp)
        
        await ctx.send("Updates made")
    
    #--------------------------------------------------------------- 
    @commands.hybrid_command(description = "Add an item to your to-do list") 
    @app_commands.describe(goal='Item to add to to-do list')
    async def add_todo(self, ctx:discord.Interaction, goal : str):
        user_id = ctx.author.id
        user_name = ctx.author.name
        
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)

        
        if user_id not in todoDatas:
            databaseCommands.create_user_todo(user_id, user_name)
            
        userData = todoDatas[user_id]
         
        userData.to_do.append(goal)

        with open("todoDatas.pkl", 'wb') as fp:
            pickle.dump(todoDatas, fp)
        await ctx.send("To-Do bullet added")
    
    #---------------------------------------------------------------
    
    @commands.hybrid_command(description = "Add an item to your deadline list.")
    @app_commands.describe(deadline_date='Format date as m/d')
    @app_commands.describe(deadline_description='Item to add to deadlines')
    async def add_deadline(self, ctx:discord.Interaction, deadline_date : str, deadline_description : str):
        user_id = ctx.author.id
        user_name = ctx.author.name
        
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)

        
        if user_id not in todoDatas:
            databaseCommands.create_user_todo(user_id, user_name)
            
        userData = todoDatas[user_id]
         
        userData.deadlines[deadline_description] = deadline_date

        with open("todoDatas.pkl", 'wb') as fp:
            pickle.dump(todoDatas, fp)
        await ctx.send("To-Do bullet added")
    
    #---------------------------------------------------------------
    
    @commands.hybrid_command(description = "Remove an item from your to-do list")
    @app_commands.describe(number_item='Format date as m/d')
    @app_commands.describe(column='Input "left" or "right" for the column')
    async def remove_todo(self, ctx:discord.Interaction, number_item: int, column: str):
        
        user_id = ctx.author.id
        user_name = ctx.author.name
        
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)
        
        
        if user_id not in todoDatas:
            databaseCommands.create_user_todo(user_id, user_name)
            
        userData = todoDatas[user_id]
        if (column.lower() == "left"):
            items = list(userData.to_do)
            print(len(items))
            if (number_item - 1 >= len(items)):
                await ctx.send("Invalid input")
            entry = items[number_item - 1]
            print(entry)
            del userData.to_do[number_item - 1]
            
            with open("todoDatas.pkl", 'wb') as fp:
                pickle.dump(todoDatas, fp)
            await ctx.send("Entry successfully deleted")
            return
        elif (column.lower() == "right"):
            items = list(userData.deadlines)
            if (number_item - 1 >= len(items)):
                await ctx.send("Invalid input")
            entry = items[number_item - 1]
            userData.to_do.pop(entry)
            
            with open("todoDatas.pkl", 'wb') as fp:
                pickle.dump(todoDatas, fp)
            await ctx.send("Entry successfully deleted")
            return
        else:
             await ctx.send("Invalid input")
        

        
        
    
    #---------------------------------------------------------------
           
    @commands.hybrid_command(description = "View your ToDo list")
    async def todo_list(self, ctx: commands.Context):
        user_id = ctx.author.id
        
        todoDatas = {}
        with open("todoDatas.pkl", 'rb') as fp:
            todoDatas = pickle.load(fp)
        
        if user_id not in todoDatas:
            user_name = ctx.author.name
            databaseCommands.create_user_todo(user_id, user_name)
            
        userData = todoDatas[user_id]
        
        #image is 1280x768
        backgroundPath = "C:/CodingProjects/DiscBot/images/todo.jpg"
        if (userData.background != "C:/CodingProjects/DiscBot/images/todo.jpg"):
            img = requests.get(userData.background).content
            imgPath = "C:\CodingProjects\DiscBot\images/tempBackground.jpg"
            with open(imgPath, 'wb') as handler:
                handler.write(img)
                handler.close()

            #resize image to 1280x768
            im = Image.open(imgPath)
            #im1 = im.crop((0, 80, 1280, 580))
            im2 = im.resize((1280, 580))

            im2.save(imgPath)
            backgroundPath = imgPath
        
        background = Editor(backgroundPath)
        avatar_url = ctx.author.avatar.url 
        img = requests.get(avatar_url).content
        with open("C:\CodingProjects\DiscBot\images/tempAvatar.jpg", 'wb') as handler:
            handler.write(img)
            handler.close()

        avatar = "C:\CodingProjects\DiscBot\images/tempAvatar.jpg"
        profile = Editor(avatar).resize((75, 75)).circle_image()

        # To use users profile picture load it from url
        # using the load_image/load_image_async function
        # profile_image = load_image(str(ctx.author.avatar_url))
        # profile = Editor(profile_image).resize((150, 150)).circle_image()


        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)
        poppins_tiny = Font.poppins(size=15)

        #create clear shape in corner if desired
        #card_right_shape = [(400, 0), (520, 337), (600, 337), (600, 0)]
        #background.polygon(card_right_shape, "#2C2F33")

        background.paste(profile, (30, 20))

        #progress bar
        #background.rectangle(
        #    (30, 220), width=750, height=40, fill="#494b4f", radius=20
        #)

        background.text((125, 30), userData.leftHeader, font=poppins, color=userData.textColor)
        background.rectangle((125, 75), width=450, height=2, fill="#17F3F6")
        time = datetime.now()
        background.text((125, 90), str(time.strftime('%B')) + " " + str(time.day) + ", " + str(time.strftime('%Y')), font=poppins_small, color=userData.textColor)

        background.text((725, 30), userData.rightHeader, font=poppins, color=userData.textColor)
        background.rectangle((725, 75), width=450, height=2, fill="#17F3F6")


        #Fill with to do list
        if len(userData.to_do) > 0:
            for i in range(len(userData.to_do)):
                background.text(
                    (45, 150+(60*i)),
                    userData.to_do[i],
                    font=poppins_small,
                    color=userData.textColor,
                )
                
        i = 0
        if len(userData.deadlines) > 0:
            for deadline, date in userData.deadlines.items():
                background.text(
                    (725, 150+(60*i)),
                    userData.deadlines[deadline] + ": " + deadline,
                    font=poppins_small,
                    color=userData.textColor,
                )
                i += 1
                
            
            
        #cannot write mode rgba as jpeg, so first convert rgba to rgb
        img = background.image
        new_img = img.convert('RGB')
        new_img.save("C:\CodingProjects\DiscBot\images/todo_returner.jpg")
        
        #with open("C:\CodingProjects\DiscBot\images/todo_returner.jpg", 'rb') as f:
        #    final_todo_list = discord.File(f)
        final_todo_list = discord.File("C:\CodingProjects\DiscBot\images/todo_returner.jpg")
        await ctx.send(file=final_todo_list)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(databaseCommands(bot))
    
    
    
class ToDo: 
        messages = {}
        Name = ""
        to_do = {}
        deadlines = {}
        background = ""
        leftHeader = ""
        rightHeader = ""
        textColor = ""
        
        def __init__(self):
            self.messages = []
            self.name = ""
            self.deadlines = {}
            self.to_do = []
            self.background = "C:/CodingProjects/DiscBot/images/todo.jpg"
            self.rightHeader = ""
            self.leftHeader = ""
            self.textColor = "white"
            
todoDatas = {}




