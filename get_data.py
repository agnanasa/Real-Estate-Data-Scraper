import sqlite3
import requests

# Connect to SQLite database
conn = sqlite3.connect('real_data.db')
cur = conn.cursor()

# API endpoint and headers
API_KEY = '3d1be771629545c8a30bdb267976dca4'
BASE_URL = 'https://api.rentcast.io/v1/properties'
params = {
    'city': 'Glendale',
    'state': 'AZ',
    'limit': 500  # You can adjust the limit as needed
}
headers = {
    'X-Api-Key': API_KEY
}

# Fetch data from the RentCast API
response = requests.get(BASE_URL, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    
    # Assuming data is a list of property dictionaries
    for property in data:
        # Check if the property already exists
        cur.execute('''
        SELECT id FROM properties WHERE address_line1 = ? AND zip_code = ?
        ''', (property['addressLine1'], property['zipCode']))
        
        if cur.fetchone() is None:
            # Insert property data if it does not exist
            cur.execute('''
            INSERT INTO properties (address_line1, address_line2, city, state, zip_code, county, latitude, longitude, property_type, bedrooms, bathrooms, square_footage, lot_size, year_built, assessor_id, legal_description, subdivision, zoning, last_sale_date, last_sale_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (property['addressLine1'], property.get('addressLine2'), property['city'], property['state'], property['zipCode'], property.get('county'), property.get('latitude'), property.get('longitude'), property.get('propertyType', 'Unknown'), property.get('bedrooms'), property.get('bathrooms'), property.get('squareFootage'), property.get('lotSize'), property.get('yearBuilt'), property.get('assessorID'), property.get('legalDescription'), property.get('subdivision'), property.get('zoning'), property.get('lastSaleDate'), property.get('lastSalePrice')))

            property_id = cur.lastrowid

            # Insert features data
            features = property.get('features', {})
            cur.execute('''
            INSERT INTO features (property_id, architecture_type, cooling, cooling_type, exterior_type, floor_count, foundation_type, garage, garage_type, heating, heating_type, pool, roof_type, room_count, unit_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (property_id, features.get('architectureType'), features.get('cooling'), features.get('coolingType'), features.get('exteriorType'), features.get('floorCount'), features.get('foundationType'), features.get('garage'), features.get('garageType'), features.get('heating'), features.get('heatingType'), features.get('pool'), features.get('roofType'), features.get('roomCount'), features.get('unitCount')))

            # Insert tax assessments data
            for year, assessment in property.get('taxAssessments', {}).items():
                cur.execute('''
                INSERT INTO tax_assessments (property_id, year, value, land_value, improvements_value)
                VALUES (?, ?, ?, ?, ?)
                ''', (property_id, year, assessment.get('value'), assessment.get('land'), assessment.get('improvements')))

            # Insert property taxes data
            for year, taxes in property.get('propertyTaxes', {}).items():
                cur.execute('''
                INSERT INTO property_taxes (property_id, year, total)
                VALUES (?, ?, ?)
                ''', (property_id, year, taxes.get('total')))

            # Insert owner data
            owner = property.get('owner', {})
            cur.execute('''
            INSERT INTO owners (property_id, name, mailing_address_line1, mailing_address_line2, mailing_city, mailing_state, mailing_zip_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (property_id, owner.get('names', [None])[0], owner.get('mailingAddress', {}).get('addressLine1'), owner.get('mailingAddress', {}).get('addressLine2'), owner.get('mailingAddress', {}).get('city'), owner.get('mailingAddress', {}).get('state'), owner.get('mailingAddress', {}).get('zipCode')))

    # Commit the transaction
    conn.commit()
else:
    print(f"Failed to fetch data: {response.status_code}")

# Close the cursor and connection
cur.close()
conn.close()