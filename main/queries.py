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

        # Query to find businesses within the specified distance (using SRID 3857 for meter-based distance)
        query = '''
        SELECT name, ST_Y(geom::geometry) AS latitude, ST_X(geom::geometry) AS longitude, relevancy_score
        FROM businesses
        WHERE ST_DWithin(
            ST_Transform(geom, 3857),  -- Transform to SRID 3857 for meter-based distance
            ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 3857),
            %s
        )
        ORDER BY relevancy_score DESC
        LIMIT 15;
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
