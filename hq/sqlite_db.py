import sqlite3

def get_readonly_connection(db_path):
    return sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)



# sqlite_db = "/home/sarai/Documents/02 Areas/digital_life/habits/Loop Habits Backup 2021-04-24 130112.db"

# con = sqlite3.connect(sqlite_db)

# cur = con.cursor()
# cur.execute("select sql from sqlite_master where type = 'table';")
# print(cur.fetchall())


# cur.execute("SELECT * FROM Habits;")
# cur.fetchone()
# [d[0] for d in cur.description]

# cur.execute("SELECT COUNT(*) FROM Habits;")
# cur.fetchone()


# cur.execute("SELECT Rep.id, Rep.timestamp, Rep.value, Hab.description, Hab.name FROM Repetitions AS Rep INNER JOIN Habits AS Hab ON Hab.Id = Rep.id;")
