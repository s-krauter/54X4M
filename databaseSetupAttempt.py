import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()
#sqlite_master holds table of all tables, useful

print(cur.execute("SELECT Question, Category FROM trivia WHERE Category = 'brain' LIMIT 2").fetchall())

strg = open('trivia/brain-teasers.txt', 'r').read()
#print(str)

trim = strg.split('#')
category = "brain"

question = ""
answer = ""
optionA = ""
optionB = ""
optionC = ""
optionD = ""

for i in range(1, len(trim)):
    val = trim[i].split('\n')
    #print(val)
    question = ""
    answer = ""
    optionA = ""
    optionB = ""
    optionC = ""
    optionD = ""
    
    if len(val[0]) > 2:
        question = val[0][2:]
    else:
        question = ""
        
    if len(val[1]) > 2:
        answer = val[1][2:]
    else:
        answer = ""
        
    if len(val[2]) > 2:
        optionA = val[2][2:]
    else:
        optionA = ""
        
    if len(val[3]) > 2:
        optionB = val[3][2:]
    else:
        optionB = ""
        
    if len(val[4]) > 2:
        optionC = val[4][2:]
    else:
        optionC = "" 
        
    if len(val[5]) > 2:
        optionD = val[5][2:]
    else:
        optionD = ""     

    params = (category, question, answer, optionA, optionB, optionC, optionD)
    #cur.execute("INSERT INTO trivia(Category, Question, Answer, OptionA, OptionB, OptionC, OptionD) VALUES(?, ?, ?, ?, ?, ?, ?)", params)        

con.commit()
#for i in range(1, len(trim)):
    
    



#cur.execute("INSERT INTO Jackbox(user_id, funniness, unfunniness, guild_id) VALUES('name', 'fun', 'unfun', 'guild');")
#response = cur.execute("SELECT user_id FROM Jackbox")

#response = cur.execute("SELECT user_id FROM Jackbox")
#response = cur.execute("CREATE TABLE yo_mama(counter, guild_id)")
#print(response.fetchall()[0])