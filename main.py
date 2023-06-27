import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import sys
import tokenFile

from cogs.Core_Commands_Cog import Core_Commands
from cogs.Fun import Fun
from cogs.music import Music

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='/', intents=intents)

#word scrambler 
import requests
import random
from discord.ext import tasks, commands
import asyncio
import time
            
#Ping Command        
@bot.tree.command(name = "ping", description = "Ping the bot and get response time.")
async def ping(interaction) -> None:
     await interaction.response.send_message(f'Pongers! {round(bot.latency * 1000)}ms response time')

  
#bot online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.add_cog(Core_Commands(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Music(bot))
     
     
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    
#Unscramble Minigame        
@bot.tree.command(name = "word_scramble", description = "Unscramble a word before time runs out!")
async def word_scramble(interaction) -> None:        
    #load dict of words
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

    response = requests.get(word_site)
    WORDS = response.content.splitlines()

    idx = random.randint(0, 9999)

    word = str(WORDS[idx])[2:-1]

    #find words of 8 letters or more
    while len(word) < 8:
        idx = random.randint(0, 9999)
        word = str(WORDS[idx])[2:-1]

        
        '''#check for correct word
        def check(m: discord.Message):
            return m.content == word
        
        
    await ctx.send("Correct! The word was " + word + "!")'''

        
    #generate scrambled word
    scrambleIdx = []
    while len(scrambleIdx) < len(word):
        scrIdx = random.randint(0, len(word) - 1)
        if scrIdx not in scrambleIdx:
            scrambleIdx.append(scrIdx)
        
    scrambleStr = ""
    for i in scrambleIdx:
        scrambleStr += word[i]
        
        

    #set up initial blank word
    ansStr = ""
    for i in range(len(word)):
        ansStr += "_"
            
           
    usedIdx = []
    ansStr = []
    ##include '\\' before each underscore so that it doesn't interpret it as markdown
    for i in range(len(word)):
        ansStr.append("\\_")  
    
    #starting message
    embedStr = ""
    for i in range(len(ansStr)):
        embedStr += ansStr[i]

    embedVar = discord.Embed(title="Unscramble the word, 2 minutes left!",
                                 color=0x00ff00)
        
    embedVar.add_field(name=scrambleStr, value = embedStr)
    await interaction.response.send_message(embed=embedVar)
    
    def check(m: discord.Message):
        return m.content == word
    
    answer1 = None
    try:
        answer1 = await bot.wait_for("message", timeout= 60, check=check)
                 
    except asyncio.TimeoutError: 
        #do nothing
        pass
    
    if answer1 is not None:
        embedVar = discord.Embed(title="Correct! The word was " + word,
                                 color=0x00ff00)
        await interaction.channel.send(embed=embedVar)
        return
    
    
    #add two letters for hint 2
    while len(usedIdx) < 2:
        newIdx = random.randint(0, len(word) - 1)
        if newIdx not in usedIdx:
            usedIdx.append(newIdx)
            ansStr[newIdx] = word[newIdx] 
        
    embedStr = ""
    for i in range(len(ansStr)):
        embedStr += ansStr[i]

    embedVar = discord.Embed(title="Unscramble the word, 1 minute left!",
                                 color=0x00ff00)
        
    embedVar.add_field(name=scrambleStr, value = embedStr)
    
    await interaction.channel.send(embed=embedVar)
        
    try:
        answer2 = await bot.wait_for("message", timeout= 30, check=check)
                 
    except asyncio.TimeoutError: 
        #do nothing
        pass
    
    answer2 = None
    if answer2 is not None:
        embedVar = discord.Embed(title="Correct! The word was " + word,
                                 color=0x00ff00)
        await interaction.channel.send(embed=embedVar)
        return
        
    #add five letters for hint 3
    while len(usedIdx) < 5:
        newIdx = random.randint(0, len(word) - 1)
        if newIdx not in usedIdx:
            usedIdx.append(newIdx)
            ansStr[newIdx] = word[newIdx]
            
    embedStr = ""
    for i in range(len(ansStr)):
        embedStr += ansStr[i]

    embedVar = discord.Embed(title="Unscramble the word, 30 seconds left!",
                                 color=0x00ff00)
        
    embedVar.add_field(name=scrambleStr, value = embedStr)
    await interaction.channel.send(embed=embedVar)
        
    answer3 = None
    try:
        answer3 = await bot.wait_for("message", timeout= 30, check=check)
                 
    except asyncio.TimeoutError: 
        #do nothing
        pass
    
    if answer3 is not None:
        embedVar = discord.Embed(title="Correct! The word was " + word,
                                 color=0x00ff00)
        await interaction.channel.send(embed=embedVar)
        return
    
        
    #reveal correct answer
    embedVar = discord.Embed(title="Time is up!",
                                 color=0x00ff00)
        
    embedVar.add_field(name="Correct word:", value = word)
    await interaction.channel.send(embed=embedVar)

bot.activity = discord.Game(name='/about')
# or, for watching:
#activity = discord.Activity(name='my activity', type=discord.ActivityType.watching)


#log in to bot with token
bot.run(tokenFile.BOT_TOKEN)




