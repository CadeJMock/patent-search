import os
import json
import psycopg2
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# the database connection param
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "patent_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    """Establish a connection to the PostgreSQL database"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    conn.autocommit = True
    return conn

def insert_patents_from_json(json_file):
    """Insert patent data from a JSON file into the database"""
    try:
        # loading JSON data from the file
        with open(json_file, 'r') as file:
            patents_data = json.load(file)

        # connecting to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # insert each patent into the database
        for patent in patents_data:
            cursor.execute('''
                INSERT INTO patents (id, title, authors, date, description)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;  -- Skip if the patent ID already exists
            ''', (
                patent.get('patent_id'),
                patent.get('title'),
                ", ".join(patent.get('authors', [])),  # converting list of authors to a comma-separated string
                patent.get('date', ''),  # default to empty string if date is missing
                patent.get('description', '')  # default to empty string if description is missing
            ))

        print(f"Inserted {len(patents_data)} patents into the database.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # closing the database connection
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # the path to the JSON file containing patent data
    json_file = 'patents.json'  # replace with actual path to your JSON file

    # inserting the data from the JSON file into the database
    insert_patents_from_json(json_file)