import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('real_data.db')
cur = conn.cursor()

# Create the properties table
cur.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    county TEXT,
    latitude REAL,
    longitude REAL,
    property_type TEXT,
    bedrooms INTEGER,
    bathrooms INTEGER,
    square_footage INTEGER,
    lot_size INTEGER,
    year_built INTEGER,
    assessor_id TEXT,
    legal_description TEXT,
    subdivision TEXT,
    zoning TEXT,
    last_sale_date TEXT,
    last_sale_price REAL
)
''')

# Create the features table
cur.execute('''
CREATE TABLE IF NOT EXISTS features (
    property_id INTEGER,
    architecture_type TEXT,
    cooling INTEGER,
    cooling_type TEXT,
    exterior_type TEXT,
    floor_count INTEGER,
    foundation_type TEXT,
    garage INTEGER,
    garage_type TEXT,
    heating INTEGER,
    heating_type TEXT,
    pool INTEGER,
    roof_type TEXT,
    room_count INTEGER,
    unit_count INTEGER,
    PRIMARY KEY (property_id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
''')

# Create the tax_assessments table
cur.execute('''
CREATE TABLE IF NOT EXISTS tax_assessments (
    property_id INTEGER,
    year INTEGER,
    value REAL,
    land_value REAL,
    improvements_value REAL,
    PRIMARY KEY (property_id, year),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
''')

# Create the property_taxes table
cur.execute('''
CREATE TABLE IF NOT EXISTS property_taxes (
    property_id INTEGER,
    year INTEGER,
    total REAL,
    PRIMARY KEY (property_id, year),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
''')

# Create the owners table
cur.execute('''
CREATE TABLE IF NOT EXISTS owners (
    property_id INTEGER,
    name TEXT,
    mailing_address_line1 TEXT,
    mailing_address_line2 TEXT,
    mailing_city TEXT,
    mailing_state TEXT,
    mailing_zip_code TEXT,
    PRIMARY KEY (property_id, name),
    FOREIGN KEY (property_id) REFERENCES properties(id)
)
''')

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

