import sqlite3

conn = sqlite3.connect('trasacts.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE actions (id INTEGER PRIMARY KEY, date DATETIME, merchant_id VARCHAR(255), completed TINYINT, transaction_id VARCHAR(255), request_user_id VARCHAR(255))''')
