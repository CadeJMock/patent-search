# Patent Search

Patent Search, otherwise referred to as Patent Finder, is a web application designed to help users search, browse, and analyze patent documents. The app offers features such as keyword search, detailed patent views, and (future) AI-powered patent recommendations to simplify patent research.

## Features
- **Patent Search:** Quickly search for patents by keyword.
- **Detailed Patent Views:** Display patent information including title, authors, filing and expiration dates, and descriptions.
- **Data Visualization:** User-friendly interface to display search results.
- **Scalable Backend:** Powered by Python (Flask) and PostgreSQL to manage patent data efficiently.
- **Future Enhancements:** Planned features include AI-powered recommendations and enhanced user collaboration.<br /><br />

## Project Structure
Patent Finder/<br />
├── app.py                       # Flask backend server with API endpoints<br />
├── .env                         # Environment variables (DB credentials, port, etc.)<br />
├── requirements.txt             # Python dependencies<br />
/static/<br />
  ├── index.html                   # Main HTML file for the front-end interface<br />
  ├── script.js                    # JavaScript to handle search and API calls<br />
  ├── styles.css                   # CSS styles for the application<br />
/data scrapper/<br />
  ├── Patent scraped data.py         # Script to process raw patent data from XML to JSON<br />
  /Patent Extracted Data/<br />
    ├── ipg240102.xml                # Any .xml file from "https://bulkdata.uspto.gov/"<br /> 
                                     # "Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)"<br />
    ├── ipg240102_interim_x.json     # Multiple intermediate processed data files, x is multiples of 1000<br />
    ├── ipg240102.json               # Sample processed patent data (JSON format)<br /><br />


## Technology Stack
- **Backend:** Python, Flask, psycopg2
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Environment Management:** python-dotenv
- **Data Processing:** Custom Python scripts for converting XML patent data into JSON<br /><br />

## Installation
1. **Clone Repository:**<br />
*git clone https://git clone https://github.com/CaeJMock/patent-search.git*<br />
*cd patent-search*<br /><br />
2. **Set Up Virtual Environment:**<br />
*python -m venv venv*<br />
*source venv\Scripts\activate* (on Windows)<br /><br />
3. **Install Dependencies:**<br />
*pip install -r requirements.txt*<br /><br />
4. **Configure Environment Variables:**<br />
Update the .env files with your database credentials and desire configuration:<br />
*DB_HOST=localhost # default host<br />
DB_NAME=yourdatabase<br />
DB_USER=postgres # default username<br />
DB_PASS=yourpassword<br />
DB_PORT=5432 # default database port <br />
PORT=5000 #default port*<br /><br />
5. **Initialize the Database:**<br />
Ensure PostgreSQL is installed and running. The Flask app automatically creates the necessary table and inserts dummy data if the database is empty.<br />

## Running the Applicaton
Start the Flask server:<br />
*python app.py*<br />
Then, open your browser and navigate to *http://localhost:5000* to use the application.<br /><br />

## Data Processing
The "*Patent scraped data.py*" script handles the conversion of raw patent XML data into a JSON format. This data (stored in "*ipg240102.json*") is used for populating the patent database and demonstrating the search functionality.<br /><br />

## Authors
- **Team Members:** Kathleen Sachez, Cade Mock, Cole Mattern, Alex Pittman, Darrnell Lampkin, Parker Jung, and Charan Jagwani
