import sqlite3



def txtIntoDatabase(path, categoryToSet):
    

    con = sqlite3.connect('database.db')

    cur = con.cursor()
    #sqlite_master holds table of all tables, useful

    #print(cur.execute("SELECT Question, Category FROM trivia WHERE Category = 'brain' LIMIT 2").fetchall())

    strg = open(path, 'r', encoding = "utf8").read()
    #print(str)

    trim = strg.split('#')
    category = categoryToSet

    question = ""
    answer = ""
    optionA = ""
    optionB = ""
    optionC = ""
    optionD = ""

    '''string = trim[206]
    trimmer = string.split("^")

    print(trimmer[0])
    trimmerB = trimmer[1].split('\n')
    for i in range(0, len(trimmerB)): 
        if len(trimmerB[i]) >= 1:
            trimmerB[i] = trimmerB[i][1:]
            trimmerB[i] = trimmerB[i].lstrip()
    print(trimmerB)'''



    for i in range(1, len(trim)):
        string = trim[i]
        trimmer = string.split("^")
        print(trimmer)
        trimmerB = trimmer[1].split('\n')
        for j in range(0, len(trimmerB)): 
            if len(trimmerB[j]) >= 1:
                trimmerB[j] = trimmerB[j][1:]
                trimmerB[j] = trimmerB[j].lstrip()

        #print(val)
        if len(trimmer[0]) > 1:
            trimmer[0] = trimmer[0][2:]

        question = trimmer[0]
        answer = ""
        optionA = ""
        optionB = ""
        optionC = ""
        optionD = ""
        print(trimmerB)


        answer = trimmerB[0]

        optionA = trimmerB[1]

        optionB = trimmerB[2]

        if len(trimmerB) >= 4:
            optionC = trimmerB[3]

        if len(trimmerB) >= 5:
            optionD = trimmerB[4]


        params = (category, question, answer, optionA, optionB, optionC, optionD)

        #print(params)
        cur.execute("INSERT INTO trivia(Category, Question, Answer, OptionA, OptionB, OptionC, OptionD) VALUES(?, ?, ?, ?, ?, ?, ?)", params)        

    con.commit()
    #for i in range(1, len(trim)):





    #cur.execute("INSERT INTO Jackbox(user_id, funniness, unfunniness, guild_id) VALUES('name', 'fun', 'unfun', 'guild');")
    #response = cur.execute("SELECT user_id FROM Jackbox")

    #response = cur.execute("SELECT user_id FROM Jackbox")
    #response = cur.execute("CREATE TABLE yo_mama(counter, guild_id)")
    #print(response.fetchall()[0])
    
txtIntoDatabase('trivia/video-games.txt', 'games')