import sqlite3


# Connect to SQLite database
conn = sqlite3.connect('real_data.db')
# Create a cursor object
cur = conn.cursor()

# Execute the SELECT query
cur.execute("SELECT * FROM properties")

# Fetch all rows from the executed query
rows = cur.fetchall()

# Process the results
for row in rows:
    print(row)
