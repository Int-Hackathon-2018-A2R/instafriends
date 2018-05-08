import sqlite3
connection = sqlite3.connect("instafriends.db")
cursor = connection.cursor()
'''cursor.execute("DROP TABLE USERS;")
cursor.execute("DROP TABLE tokens;")

sql_command = """
CREATE TABLE users ( 
id INTEGER PRIMARY KEY, 
name VARCHAR(150),
vk INTEGER,
phone INTEGER,
email VARCHAR(50),
vk_token VARCHAR(50));"""

cursor.execute(sql_command)

sql_command = """
CREATE TABLE tokens (
id INTEGER PRIMARY KEY,
token VARCHAR(30),
user_id INTEGER,
timestamp INTEGER);
"""
cursor.execute(sql_command)
'''

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
connection.commit()
connection.close()