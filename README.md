# USPTO Patent Search Web Application

Our USPTO Patent Search Web Application, is a web application designed to help users search, browse, and analyze patent documents. The app offers features such as keyword search, detailed patent views, and AI-powered patent recommendations to simplify patent research.

## Features
- **Patent Search:** Quickly search for patents by keyword, ID, author, or date.
- **Detailed Patent Views:** Display patent information including title, authors, filing and expiration dates, and descriptions.
- **Smart Recommendations:** AI-powered similar patent recommendations using content-based filtering.
- **Data Visualization:** User-friendly interface to display search results.
- **Scalable Backend:** Powered by Python (Flask) and PostgreSQL to manage patent data efficiently.
- **Future Enhancements:** Planned features include enhanced user collaboration.

## Project Structure
```
patent-search/
├── app.py                         # Flask backend server with API endpoints
├── .env                           # Environment variables (DB credentials, port, etc.)
├── .gitignore                     # Git ignore file
├── gitignore.txt                  # Alternative gitignore file
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
│
├── data scrapper/                 # Data processing directory
│   ├── Extracted Patent Data/     # Directory for processed patent data
│   ├── insert_patents_from_json.py # Script to insert processed data into PostgreSQL
│   └── scrape_patent_data.py      # Script to process raw patent data from XML to JSON
│
├── static/                        # Frontend assets
│   ├── resources/                 # Resource files
│   │   └── Fish.png               # Logo image
│   ├── index.html                 # Main HTML file for the front-end interface
│   ├── script.js                  # JavaScript to handle search and API calls
│   └── styles.css                 # CSS styles for the application
│
└── venv/                          # Virtual environment (not tracked in git)
```

## Technology Stack
- **Backend:** Python, Flask, psycopg2
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Environment Management:** python-dotenv
- **Data Processing:** Custom Python scripts for converting XML patent data into JSON
- **Machine Learning:** scikit-learn for recommendation system (similarity matching)

## Installation
1. **Clone Repository:**
   ```
   git clone https://github.com/CadeJMock/patent-search.git
   cd patent-search
   ```

2. **Set Up Virtual Environment:**
   ```
   python -m venv venv
   source venv/Scripts/activate  # on Windows
   ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Update the .env file with your database credentials and desired configuration:
   ```
   DB_HOST=localhost  # default host
   DB_NAME=patentfinder  # your postgresql database name
   DB_USER=postgres  # default username
   DB_PASS=yourpassword  # your chosen postgresql password
   DB_PORT=5432  # default database port
   PORT=5000  # default application port
   ```

5. **Initialize the Database:**
   Ensure PostgreSQL is installed and running. The Flask app automatically creates the necessary table and inserts dummy data if the database is empty.

## Running the Application
1. Start the Flask server:
   ```
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000` to use the application.

## Data Processing
The `scrape_patent_data.py` script handles the conversion of raw patent XML data into a JSON format. This data (stored in a .json file) is then used for populating the patent database using the `insert_patents_from_json.py` script.

To get a correct XML file to process:
1. Head to "https://bulkdata.uspto.gov/" 
2. Download a zip file under the section "Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)."
3. Unzip the file into the "data scrapper" folder
4. Run the `scrape_patent_data.py` file
   - The script will prompt you to select an XML file
   - It will process the file and generate JSON output in the "Extracted Patent Data" folder
   - Interim files are created every 1000 patents to avoid memory issues
5. After processing, use `insert_patents_from_json.py` to load the processed data into your database
   - The script will prompt you to select a JSON file to import
   - The patents will be added to your PostgreSQL database

## Patent Recommendation System
The application includes a content-based recommendation system that finds similar patents based on their content. When viewing a patent, you can see up to 5 similar patents recommended by:

1. Combined title and description text analysis using TF-IDF vectorization
2. Cosine similarity calculations between patents
3. Threshold-based filtering to ensure relevance

## Authors
- **Team Lead:** Cade Mock
- **Team Members:** Kathleen Sachez, Cole Mattern, Alex Pittman, Darrnell Lampkin, Parker Jung, and Charan Jagwani
