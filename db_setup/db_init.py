import json
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'nbhd',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create the table with PostGIS extension if it doesn't exist
cur.execute('''
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS businesses (
    business_id VARCHAR(512) PRIMARY KEY,
    name VARCHAR(512),
    address VARCHAR(512),
    state VARCHAR(512),
    postal_code VARCHAR(20),
    latitude FLOAT,
    longitude FLOAT,
    geom GEOMETRY(Point, 4326),  -- Example column for storing point data with PostGIS
    stars FLOAT,
    attributes JSONB,
    categories VARCHAR(512),
    hours JSONB
);
''')
conn.commit()

# Load and insert data from JSON file
with open('businesses.json', 'r', encoding='utf-8') as file:
    try:
        for line in file:
            data = json.loads(line.strip())
            
            # Skip entry if is_open is 0 or city is not Philadelphia
            if data.get('is_open') == 0 or data.get('city') != 'Philadelphia':
                continue

            # Convert attributes and hours to JSON-formatted strings
            data['attributes'] = json.dumps(data['attributes'])
            data['hours'] = json.dumps(data['hours']) if data['hours'] else None

            # Example: Inserting spatial data into 'geom' column
            if 'latitude' in data and 'longitude' in data:
                point = f"POINT({data['longitude']} {data['latitude']})"
                cur.execute('''
                INSERT INTO businesses (
                    business_id, name, address, state, postal_code,
                    latitude, longitude, geom, stars, attributes, categories, hours
                ) VALUES (
                    %(business_id)s, %(name)s, %(address)s, %(state)s, %(postal_code)s,
                    %(latitude)s, %(longitude)s, ST_SetSRID(ST_GeomFromText(%(point)s), 4326),
                    %(stars)s, %(attributes)s::jsonb, %(categories)s, %(hours)s::jsonb
                )
                ON CONFLICT (business_id) DO NOTHING;
                ''', {'point': point, **data})

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON line: {e}")
    except psycopg2.Error as e:
        print(f"Database error: {e}")

conn.commit()

# Close the connection
cur.close()
conn.close()