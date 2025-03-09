# Patent Search

Patent Search, otherwise referred to as Patent Finder, is a web application designed to help users search, browse, and analyze patent documents. The app offers features such as keyword search, detailed patent views, and (future) AI-powered patent recommendations to simplify patent research.

## Features
- **Patent Search:** Quickly search for patents by keyword.
- **Detailed Patent Views:** Display patent information including title, authors, filing and expiration dates, and descriptions.
- **Data Visualization:** User-friendly interface to display search results.
- **Scalable Backend:** Powered by Python (Flask) and PostgreSQL to manage patent data efficiently.
- **Future Enhancements:** Planned features include AI-powered recommendations and enhanced user collaboration.

## Project Structure
Patent Finder/
├── app.py                       # Flask backend server with API endpoints
├── .env                         # Environment variables (DB credentials, port, etc.)
├── requirements.txt             # Python dependencies
/static/
  ├── index.html                   # Main HTML file for the front-end interface
  ├── script.js                    # JavaScript to handle search and API calls
  ├── styles.css                   # CSS styles for the application
/data scrapper/
  ├── Patent scraped data.py         # Script to process raw patent data from XML to JSON
  /Patent Extracted Data/
    ├── ipg240102.xml                # Any .xml file from "https://bulkdata.uspto.gov/" 
                                     # "Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)"
    ├── ipg240102_interim_x.json     # Multiple intermediate processed data files, x is multiples of 1000 
    ├── ipg240102.json               # Sample processed patent data (JSON format)


## Technology Stack
- **Backend:** Python, Flask, psycopg2
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Environment Management:** python-dotenv
- **Data Processing:** Custom Python scripts for converting XML patent data into JSON

## Installation
1. **Clone Repository:**
*git clone https://git clone https://github.com/CaeJMock/patent-search.git*
*cd patent-search*
2. **Set Up Virtual Environment:**
*python -m venv venv*
*source venv\Scripts\activate* (on Windows)
3. **Install Dependencies:**
*pip install -r requirements.txt*
4. **Configure Environment Variables:**
Update the .env files with your database credentials and desire configuration:
*DB_HOST=localhost 
DB_NAME=patentfinder
DB_USER=postgres
DB_PASS=yourpassword
DB_PORT=5432
PORT=5000*
5. **Initialize the Database:**
Ensure PostgreSQL is installed and running. The Flask app automatically creates the necessary table and inserts dummy data if the database is empty.

## Running the Applicaton
Start the Flas server:
*python app.py*
Then, open your browser and navigate to *http://localhost:5000* to use the application.

## Data Processing
The *Patent scraped data.py* script handles the conversion of raw patent XML data into a JSON format. This data (store in *ipg240102.json*) is used for populating the patent database and demonstrating the search functionality.

## Authors
- **Team Members:** Kathleen Sachez, Cade Mock, Cole Mattern, Alex Pittman, Darrnell Lampkin, Parker Jung, and Charan Jagwani
