import sqlite3
import requests

# Connect to SQLite database
conn = sqlite3.connect('real_data.db')
cur = conn.cursor()

# API endpoint and headers
API_KEY = '3d1be771629545c8a30bdb267976dca4'
PROPERTIES_URL = 'https://api.rentcast.io/v1/properties'
LISTINGS_URL = 'https://api.rentcast.io/v1/listings/sale'
headers = {
    'X-Api-Key': API_KEY
}

# Parameters for both requests
params = {
    'city': 'Glendale',
    'state': 'AZ',
    'limit': 500  # Adjust the limit as needed
}

# Fetch property data from the /properties endpoint
properties_response = requests.get(PROPERTIES_URL, headers=headers, params=params)
properties_data = properties_response.json() if properties_response.status_code == 200 else []

# Fetch listing data from the /listings/sale endpoint
listings_response = requests.get(LISTINGS_URL, headers=headers, params=params)
listings_data = listings_response.json() if listings_response.status_code == 200 else []

# Create a dictionary from listings data with a key based on address or unique ID
listings_dict = {}
for listing in listings_data:
    address = listing['addressLine1'] + listing['zipCode']
    listings_dict[address] = {
        'days_on_market': listing.get('daysOnMarket', 0),  # Store daysOnMarket using a unique key
        'price': listing.get('price', 0)  # Store price, default to 0 if not available
    }

# Iterate through properties data and match with listings data
for property in properties_data:
    # Create a matching key
    address_key = property['addressLine1'] + property['zipCode']
    
    # Check if the property type is "Single Family"
    if property.get('propertyType') == 'Single Family':
        # Get days on market and price from the listings data
        listing_info = listings_dict.get(address_key, {'days_on_market': 0, 'price': 0})
        days_on_market = listing_info['days_on_market']
        price = listing_info['price']
        
        # Check if the record already exists
        cur.execute('''
        SELECT id FROM properties WHERE address_line1 = ? AND zip_code = ?
        ''', (property['addressLine1'], property['zipCode']))
        existing_record = cur.fetchone()
        
        if existing_record is None:
            # Insert combined data into the database if it doesn't already exist
            cur.execute('''
            INSERT INTO properties (address_line1, city, state, zip_code, property_type, bedrooms, bathrooms, square_footage, price, days_on_market)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                property['addressLine1'], property['city'], property['state'], property['zipCode'], 
                property['propertyType'], property.get('bedrooms'), property.get('bathrooms'), 
                property.get('squareFootage'), price, days_on_market)
            )
            print(f"Inserted: {property['addressLine1']}, {property['zipCode']}")
        else:
            print(f"Duplicate found: {property['addressLine1']}, {property['zipCode']} - Skipping insertion")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data inserted successfully.")
