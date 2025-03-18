import os
import json
import psycopg2
from dotenv import load_dotenv
import tkinter as tk               # tkinter for selecting the JSON file location
from tkinter import filedialog     # ^ using filedialog

# load environment variables from .env file
load_dotenv()

# the database connection param
# remember to change your specific .env file to your database params
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
    # initialize these to None to start in case exceptions occur
    conn = None
    cursor = None

    try:
        # loading JSON data from the file - UTF-8 encoding
        with open(json_file, 'r', encoding="utf-8") as file:
            patents_data = json.load(file)

        # connecting to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # insert each patent into the database
        for patent in patents_data:
            cursor.execute('''
                INSERT INTO patents (id, title, authors, description)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;  -- Skip if the patent ID already exists
            ''', (
                patent.get('patent_id'),
                patent.get('title'),
                ", ".join(patent.get('authors', [])),  # converting list of authors to a comma-separated string
                # patent.get('date', ''),  # default to empty string if date is missing - commenting out for now since the json doesn't have dates currently
                patent.get('description', '')  # default to empty string if description is missing
            ))

        print(f"Inserted {len(patents_data)} patents into the database.")
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    except UnicodeDecodeError as e:
        print(f"Character encoding error: {e}")
        print("Try using different encoding or fixing the JSON file encoding.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    
    json_file = filedialog.askopenfilename( # open file dialog
        title="Select a compatible JSON file",
        initialdir="Extracted Patent Data", # important to allow the file dialog to see the .json files
        filetypes=(
            ("JSON files", "*.json *.JSON"), # limit the selection to JSON files
            ("All files", "*.*")
        )
    )

    root.destroy() # kill the tkinter window
    
    if json_file:
        print(f"Selected file: {json_file}")
        # inserting the data from the JSON file into the database
        insert_patents_from_json(json_file)
    else:
        print("No file was selected. Exiting")