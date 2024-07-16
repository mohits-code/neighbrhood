import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'nbhd',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Function to find businesses within a certain distance from a given location
def find_businesses_within_distance(latitude, longitude, distance):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Query to find businesses within the specified distance (using SRID 3857 for meters)
        query = '''
        SELECT name
        FROM businesses
        WHERE ST_DWithin(
            ST_Transform(geom, 3857),  -- Transform to SRID 3857 for meter-based distance
            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 3857),
            %s
        );
        '''

        # Execute the query
        cur.execute(query, (longitude, latitude, distance))
        results = cur.fetchall()

        # Close the connection
        cur.close()
        conn.close()

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    # Example usage
    latitude = 39.9526   # Replace with your actual latitude
    longitude = -75.1652 # Replace with your actual longitude
    distance = 10   # Replace with the desired distance in meters

    businesses = find_businesses_within_distance(latitude, longitude, distance)
    for business in businesses:
        print(business)

if __name__ == "__main__":
    main()
