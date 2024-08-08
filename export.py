import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('real_data.db')

# Read data from the properties table into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM properties", conn)

# Export the DataFrame to an Excel file
df.to_excel("properties_data.xlsx", index=False)

# Close the connection
conn.close()

print("Data exported successfully to properties_data.xlsx")
