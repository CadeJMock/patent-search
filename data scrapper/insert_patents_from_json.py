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
DB_NAME = os.getenv("DB_NAME", "patents")
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

def format_patent_date(date_str):
    """
    Format patent date from YYYYMMDD to YYYY-MM-DD for PostgreSQL
    
    Args:
        date_str: String containing date in YYYYMMDD format
        
    Returns:
        Formatted date string or None if invalid
    """
    print(f"Formatting date: {date_str}, type: {type(date_str)}")
    
    if not date_str or len(date_str) != 8:
        return None
        
    try:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    except (ValueError, IndexError):
        print(f"Warning: Invalid date format: {date_str}")
        return None

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
        
        # count successfully inserted patents
        success_count = 0
        # count patents skipped due to formatting issues
        skipped_count = 0

        # insert each patent into the database
        for patent in patents_data:
            patent_date_str = patent.get('date', '')
            formatted_grant_date = None
            
            priority_date_str = patent.get('priority_date', '')
            formatted_priority_date = format_patent_date(priority_date_str)
            
            if patent_date_str:
                try:
                    if len(patent_date_str) == 8:
                        year = patent_date_str[:4]
                        month = patent_date_str[4:6]
                        day = patent_date_str[6:8]
                        formatted_grant_date = f"{year}-{month}-{day}"
                        print(f"Formatted date: {patent_date_str} -> {formatted_grant_date}")
                    else:
                        print(f"Warning: Date has unexpected format: {patent_date_str}")
                except Exception as e:
                    print(f"Error formatting date {patent_date_str}: {e}")
            
            try:
                cursor.execute('''
                    INSERT INTO patents (id, title, authors, date, description)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;  -- Skip if the patent ID already exists
                ''', (
                    patent.get('id'),
                    patent.get('title'),
                    patent.get('authors'),
                    formatted_grant_date,
                    patent.get('description', '')
                ))
                success_count += 1
            except Exception as e:
                print(f"Error inserting patent {patent.get('id')}: {e}")
                skipped_count += 1

        print(f"Inserted {success_count} patents into the database.")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} patents due to errors")
        
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