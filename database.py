import sqlite3




    

con = sqlite3.connect('database.db')

cur = con.cursor()

#print(cur.execute("SELECT DISTINCT Category FROM trivia").fetchall())

cur.execute("CREATE TABLE todo(user, userData)")

con.commit()