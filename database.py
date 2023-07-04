import sqlite3

con = sqlite3.connect('database.db')

cur = con.cursor()

print(cur.execute("SELECT DISTINCT Category FROM trivia").fetchall())

con.commit()
print("Comitted")