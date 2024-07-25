import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('real_data.db')

# Read data from the database into a DataFrame
df_properties = pd.read_sql_query("SELECT * FROM properties", conn)
df_features = pd.read_sql_query("SELECT * FROM features", conn)
df_tax_assessments = pd.read_sql_query("SELECT * FROM tax_assessments", conn)
df_property_taxes = pd.read_sql_query("SELECT * FROM property_taxes", conn)
df_owners = pd.read_sql_query("SELECT * FROM owners", conn)

# Export DataFrame to Excel file
with pd.ExcelWriter('database_export.xlsx', engine='openpyxl') as writer:
    df_properties.to_excel(writer, sheet_name='Properties', index=False)
    df_features.to_excel(writer, sheet_name='Features', index=False)
    df_tax_assessments.to_excel(writer, sheet_name='Tax Assessments', index=False)
    df_property_taxes.to_excel(writer, sheet_name='Property Taxes', index=False)
    df_owners.to_excel(writer, sheet_name='Owners', index=False)

# Close the database connection
conn.close()
