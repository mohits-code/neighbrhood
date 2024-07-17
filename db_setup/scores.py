import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'nbhd',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def update_relevancy_scores():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Add a new column 'relevancy_score' if it does not exist
        add_column_query = '''
        ALTER TABLE businesses
        ADD COLUMN IF NOT EXISTS relevancy_score DOUBLE PRECISION;
        '''
        cur.execute(add_column_query)
        conn.commit()

        # Update the relevancy score for each business
        update_scores_query = '''
        UPDATE businesses
        SET relevancy_score = (stars * review_count) / 50;
        '''
        cur.execute(update_scores_query)
        conn.commit()

        print("Relevancy scores updated successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    update_relevancy_scores()