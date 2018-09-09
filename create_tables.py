import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)
print('users table created.')

create_items_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_items_table)
print('items table created.')

#cursor.execute("INSERT INTO items VALUES ('test', 10.99)")


connection.commit()
connection.close()

