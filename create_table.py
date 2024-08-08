import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('real_data.db')
cur = conn.cursor()

# Create the properties table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_line1 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    property_type TEXT,
    bedrooms INTEGER,
    bathrooms REAL,
    square_footage INTEGER,
    price INTEGER,
    days_on_market INTEGER
)
''')

# Commit the transaction
conn.commit()

# Verify the table creation
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties';")
table_exists = cur.fetchone()
if table_exists:
    print("Table 'properties' exists.")
else:
    print("Table 'properties' does not exist.")

# Close the cursor and connection
cur.close()
conn.close()
