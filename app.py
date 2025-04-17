# RUN EVERYTHING BY DOING THE FOLLOWING:
# (terminal) -> python app.py (or run python file in a drop down)
# (web browser) -> http://localhost:5000 (do not just open the html file, it won't connect to the backend)

from flask import Flask, request, jsonify # Flask for web server, request/jsonify for handling HTTP requests/responses
import psycopg2 # PostgreSQL adapter for Python
import os # Operating system interface for environment variables
from dotenv import load_dotenv # For loading environment variables from .env file
from datetime import datetime # For date validation

# Load environment variables from .env file
# (This just allows us to keep database credentials outside of the code, change the .env file to your own names and passwords)
load_dotenv()

# initialize flask application
# static_folder='static' tells Flask where to find the static files (HTML, CSS, JS), we don't need the flask server to interact with these
# static_url_path='' makes static files available at the root URL path
app = Flask(__name__, static_folder='static', static_url_path='')

# get database connection paramteres from environment variables
# the second parameter in each getenv() is the default value if the variable isn't found
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "patents")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_PORT = os.getenv("DB_PORT", "5000")

def get_db_connection():
    """Establish a connection to the PostgreSQL database"""
    # create a connection to the PostgreSQL database using the parameters
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    # setting autocommit=True means each query will be committed immediately
    # without needing explicit transaction management
    conn.autocommit = True
    return conn

def init_db():
    """Initialize database with dummy patent data"""
    # get a connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # DROP the patents table if it exists, this is to ensure it updates with our dummy_patents data each time,
    # in case we add new information or change stuff around
    cursor.execute('DROP TABLE IF EXISTS patents')
    
    # create patents table if it doesn't exist yet
    # this table stores all patent information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patents (
            id VARCHAR(20) PRIMARY KEY,      -- Patent ID (unique identifier)
            title TEXT NOT NULL,             -- Patent title
            authors TEXT NOT NULL,           -- Authors/investors of the patent
            date DATE NOT NULL,              -- Filing date
            description TEXT                 -- Brief description of the patent
        )
    ''')
    
    # check if we already have data in the table to avoid duplicates
    cursor.execute("SELECT COUNT(*) FROM patents")
    count = cursor.fetchone()[0] # get the reuslt of COUNT(*)
    
    # only insert dummy data if the table is empty
    if count == 0:
        # Insert dummy patent records for demo
        # each record contains all the fields defined in the table schema
        dummy_patents = [
            ('US10123456', 'Improved Solar Panel with Enhanced Energy Conversion', 'John Smith, Jane Doe', 
             '2019-05-15', 'A solar panel design that increases energy conversion efficiency by 25% using a novel photovoltaic material.'),
            
            ('US10234567', 'Smart Home Automation System', 'Michael Johnson, Emily Williams', 
             '2020-02-10', 'An integrated system that connects and controls home devices through a centralized AI-powered hub.'),
            
            ('US10345678', 'Biodegradable Plastic Alternative', 'Robert Chen, Sarah Garcia', 
             '2018-11-20', 'A fully biodegradable plastic alternative made from plant cellulose that decomposes within 3 months.'),
            
            ('US10456789', 'Quantum Cryptography Method', 'David Wilson, Lisa Brown', 
             '2021-03-05', 'A secure communication method using quantum entanglement to detect eavesdropping attempts.'),
            
            ('US10567890', 'Advanced Water Filtration System', 'Thomas Anderson, Maria Rodriguez', 
             '2017-08-12', 'A portable water filtration system that removes 99.9% of contaminants using graphene-based filters.'),
            
            ('US10678901', 'Gesture-Based Computing Interface', 'Kevin Patel, Amanda Lee', 
             '2020-10-30', 'A computer interface that detects precise hand gestures for intuitive control of digital environments.'),
            
            ('US10789012', 'Artificial Neural Network for Medical Diagnosis', 'James Taylor, Sophia Martinez', 
             '2019-04-22', 'A specialized neural network designed to analyze medical imagery and assist in early disease detection.'),
            
            ('US10890123', 'Energy Efficient Refrigeration Technology', 'Christopher Davis, Olivia Wang', 
             '2018-07-08', 'A cooling system that reduces energy consumption by 40% through a novel thermodynamic cycle.'),
            
            ('US10901234', 'Augmented Reality Educational Tool', 'Richard Miller, Elizabeth Jones', 
             '2021-01-15', 'An educational platform that uses augmented reality to create interactive learning experiences.'),
            
            ('US11012345', 'Wireless Power Transmission System', 'Daniel White, Jennifer Kim', 
             '2017-12-03', 'A system for transmitting electrical power without wires using resonant inductive coupling.'),
            
            ('US11012346', 'Wireless Home Fridge', 'Cade M', 
             '2018-12-07', 'N/A'), # N/A will not be prevelant in the final project. Will remove descriptions that end up as "N/A" so it doesn't effect search
            
            ('US11032814', 'Testing System', 'John Smith', 
             '2018-2-13', '')
        ]
        
        # executemany() efficiently executes the same SQL for multiple parameter sets
        # this will insert all the dummy patents in one database operation
        cursor.executemany('''
            INSERT INTO patents (id, title, authors, date, description)
            VALUES (%s, %s, %s, %s, %s)
        ''', dummy_patents)
    
    # clsoe the cursor and connection
    cursor.close()
    conn.close()

# define route for the root URL ('/')
@app.route('/')
def index():
    """Serve the main HTML page"""
    # this sends the index.html file from the static folder to the client
    # the frontend JavaScript and CSS file will be loaded by the HTML file from there
    return app.send_static_file('index.html')

# define route for the search endpoint that accepts POST requests
@app.route('/search', methods=['POST'])
def search_patents():
    """Search for patents based on the query"""
    try:
        search_data = request.get_json()
        print(f"Search request received: {search_data}")

        # validate at least one field has content
        if not search_data or not any(v.strip() for v in search_data.values() if v):
            return jsonify({'error': 'Please provide at least one search term'}), 400

        # build the base query
        base_query = '''
            SELECT id, title, authors, date, description 
            FROM patents 
            WHERE 1=1  # Allows easy AND concatenation
        '''
        query_params = []

        # add field specific conditions
        # title search (partial match)
        if 'title' in search_data and search_data['title'].strip():
            base_query += " AND title ILIKE %s"
            query_params.append(f"%{search_data['title'].strip()}%")

        # authors search /partial match
        if 'authors' in search_data and search_data['authors'].strip():
            base_query += " AND authors ILIKE %s"
            query_params.append(f"%{search_data['authors'].strip()}%")

        # patent ID search /partial match
        if 'id' in search_data and search_data['id'].strip():
            base_query += " AND id ILIKE %s"
            query_params.append(f"%{search_data['id'].strip()}%")

        # date search (exact match with validation)
        if 'date' in search_data and search_data['date'].strip():
            try:
                datetime.strptime(search_data['date'].strip(), '%Y-%m-%d')
                base_query += " AND date = %s"
                query_params.append(search_data['date'].strip())
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"Executing query: {base_query}")
        print(f"With parameters: {query_params}")
        
        cursor.execute(base_query, query_params)
        results = cursor.fetchall()

        # format the results 
        patents = [{
            'id': row[0],
            'title': row[1],
            'authors': row[2],
            'date': row[3].strftime('%Y-%m-%d'),
            'description': row[4] if row[4] else 'No description available'
        } for row in results]
        
        cursor.close()
        conn.close()
        
        return jsonify(patents)

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database operation failed'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__': # this block only executes if the file is run directly (not imported)
    port = int(os.getenv("PORT", 5000))
    # Start the Flask web server
    # host='0.0.0.0' makes the server accessible from any IP address
    # debug=True enables some development features like auto-reloading on code changes and etc.
    init_db()  # Initialize the database with dummy data
    app.run(host='0.0.0.0', port=port, debug=True)