import os
import psycopg2
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "patents")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = os.getenv("DB_PORT", "5000")

def check_patent_ids():
    """Check the format of patent IDs in the database"""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Get a sample of patent IDs
        cursor.execute("SELECT id FROM patents LIMIT 1000")
        patent_ids = [row[0] for row in cursor.fetchall()]
        
        # Count the number of patents with IDs starting with different prefixes
        prefixes = Counter(id[:2] for id in patent_ids if len(id) >= 2)
        
        print("Patent ID prefixes (first 2 characters):")
        for prefix, count in prefixes.most_common():
            print(f"{prefix}: {count} patents")
        
        # Check for patents with IDs containing "us" (case-insensitive)
        cursor.execute("SELECT COUNT(*) FROM patents WHERE LOWER(id) LIKE '%us%'")
        us_count = cursor.fetchone()[0]
        print(f"\nTotal patents with IDs containing 'us' (case-insensitive): {us_count}")
        
        # Get a sample of patents with IDs not starting with "US10" (to exclude dummy data)
        cursor.execute("SELECT id FROM patents WHERE id NOT LIKE 'US10%' LIMIT 10")
        real_patent_ids = [row[0] for row in cursor.fetchall()]
        
        print("\nSample of real patent IDs (not starting with US10):")
        for patent_id in real_patent_ids:
            print(patent_id)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking patent IDs: {e}")

if __name__ == "__main__":
    check_patent_ids() 