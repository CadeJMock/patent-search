import os                          # for operating system functions like creating directories and handling file paths
import json                        # for encoding and decoding JSON data
import re                          # for "regular expression" operations to identify patterns in text
import xml.etree.ElementTree as ET # for processing XML data using a tree structure
from datetime import datetime      # datetime to track processing time and durations

# directory path to get .xml file
data_dir = "patent-search\data scrapper"

# get all XML files in the directory "data scrapper"
xml_files = [f for f in os.listdir(data_dir) if f.endswith('.xml')]

if xml_files:
    # use the FIRST XML file found
    xml_filename = xml_files[0]
    # create full path to xml file - containing patent data (hopefully)
    xml_file_path = os.path.join(data_dir, xml_filename)
    
    # generate the JSON filename by replacing .xml with .json
    json_filename = os.path.splitext(xml_filename)[0] + '.json'
    # create full path to json file - containing processed data
    json_file_path = os.path.join(data_dir, json_filename)
    
    print(f"Found XML file: {xml_file_path}")
    print(f"Will save to JSON file: {json_file_path}")
else:
    print("No XML files found in the 'data scrapper' directory.")
    print("Please navigate to 'https://bulkdata.uspto.gov/' and download an XML file from the section: Patent Grant Full Text Data (No Images) (JAN 1976 - PRESENT)")
    print("Then, unzip the XML file into the correct directory and rerun the program.")
    exit(1)

# create the directory structure for the output file if it doesn't already exist
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)  # exist_ok=True prevents errors if directory already exists

# initialize an empty list to store all the processed patent data dictionaries
patents_list = []

# counter to track the number of successfully processed patents
count = 0

# counter to track the number of patents that couldn't be processed due to errors (if any)
error_count = 0

# record the start time of processing to calculate total execution time later in case we need to optimize this process (took 3 minutes 49 seconds last time - Cade DESKTOP PC)
start_time = datetime.now()  # gets the current date and time

# message indicating the start of processing, including the file being processed and the start time
print(f"Starting to process {xml_file_path} at {start_time}")

# function to parse an individual patent XML document string into a structured dictionary
def parse_patent_xml(xml_string):
    """
    Parse a single patent XML document and extract key information.
    
    Args:
        xml_string: String containing the complete XML for a single patent document
    
    Returns:
        Dictionary with parsed patent data or None if parsing fails
    """
    try:
        # parse the XML string into an ElementTree object for easier navigation
        root = ET.fromstring(xml_string)  # creates a tree structure from the XML string
        
        # patent_id variable to store the patent's id once found
        patent_id = None
        # try multiple possible XML paths where the patent ID might be located
        # this makes the code more robust to different XML formats and structures (in case the formatting changes on other files)
        for path in ['.//publication-reference//document-id/doc-number', './/document-id/doc-number', './/patent-id', './/id']: # array of different paths
            id_elem = root.find(path)  # attempt to find an element at current path
            if id_elem is not None and id_elem.text:  # check if element exists and has text content
                patent_id = id_elem.text  # store the text content as the patent ID
                break  # stop searching once we've found a valid ID
        
        # title variable to store the patent's title once found
        title = None
        # try multiple possible XML paths where the title might be located
        for path in ['.//invention-title', './/title-of-invention', './/title']: # array of different paths
            title_elem = root.find(path)  # attempt to find an element at this path
            if title_elem is not None and title_elem.text:  # check if element exists and has text content
                title = title_elem.text  # store the text content as the patent title
                break  # stop searching once we've found a valid title
        
        # initialize an empty list to store the names of patent authors/inventors
        authors = []
        # try multiple possible XML paths where inventor information might be located
        for inventor_path in ['.//inventors/inventor/addressbook', './/applicants/applicant/addressbook', './/inventors/first-name']: # array of different paths
            inventors = root.findall(inventor_path)  # find all elements matching this path (multiple inventors potentially)
            if inventors:  # check if any inventors were found at this path
                for inv in inventors:  # iterate through each inventor element found
                    name_parts = []  # a list to store parts of the inventor's name
                    
                    # try to find the first name element for this inventor
                    first_name = inv.find('./first-name')
                    if first_name is not None and first_name.text:  # check if element exists and has text
                        name_parts.append(first_name.text)  # add first name to name parts list
                        
                    # try to find the last name element for this inventor
                    last_name = inv.find('./last-name')
                    if last_name is not None and last_name.text:  # check if element exists and has text
                        name_parts.append(last_name.text)  # add last name to name parts list
                        
                    # if we found any name parts for this inventor, combine them into a full name
                    if name_parts:
                        authors.append(" ".join(name_parts))  # join first and last name with a space
                
                # if we found any authors using this path, stop searching other paths (optimization)
                if authors:
                    break
        
        # initialize description variable to store the patent's description or abstract
        description = None
        # try multiple possible XML paths where the description might be located
        for path in ['.//abstract/p', './/abstract', './/description/p', './/description']: # array of different paths
            desc_elem = root.find(path)  # attempt to find an element at this path
            if desc_elem is not None and desc_elem.text:  # check if element exists and has text content
                description = desc_elem.text  # store the text content as the patent description
                if description == "\n\n": # empty descriptions are grabbed as "\n\n", setting the descriptions to an
                    description = "" # empty string will not mess with the search function
                break  # stop searching once we've found a valid description
        
        # dictionary to store all the extracted patent information
        patent_data = { # Can change the 'else ""' statement back to 'else "N/A"' later on, if we exclude "N/A" from our search function
            "patent_id": patent_id if patent_id else "",
            "title": title if title else "",
            "authors": authors if authors else "",
            "description": description if description else ""
        }
        
        # return the completed patent data dictionary
        return patent_data
    except Exception as e:
        # if any error occurs during parsing, print an error message with details
        print(f"Error parsing patent XML: {e}")
        # return None to indicate that parsing failed for this patent
        return None

try:
    # this is the main processing block, wrapped in a try-except to catch any overall errors
    
    # open the XML file for reading with UTF-8 encoding
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        # empty string to accumulate the current patent's XML content
        current_xml = ""
        
        # a flag to track whether we're currently inside a patent document, useful for later
        in_patent_doc = False
        
        # define regular expression patterns to identify the document boundaries in the XML file
        # pattern to match XML declaration tags (<?xml version="1.0" ...?>)
        xml_decl_pattern = re.compile(r'<\?xml.*?\?>')
        
        # pattern to match the start of patent documents (using multiple possible root element names)
        patent_start_pattern = re.compile(r'<(us-patent-grant|patent-document|patent).*?>')
        
        # pattern to match the end of patent documents (closing tags for possible root elements)
        patent_end_pattern = re.compile(r'</(us-patent-grant|patent-document|patent)>')
        
        # iterate through the file line by line, with line_num starting at 1
        for line_num, line in enumerate(file, 1):
            # check if this line contains a new XML declaration while already processing a document
            # this indicates the end of one document and the start of another (since the files are concated.)
            if xml_decl_pattern.search(line) and in_patent_doc:
                # we've found the end of the previous document and beginning of a new one
                
                # process the previous document if it's not empty
                if current_xml.strip():  # check if there's actual content after removing whitespace
                    # parse the accumulated XML string into a patent data dictionary
                    patent_data = parse_patent_xml(current_xml)
                    
                    # if parsing was successful (returns None if not)
                    if patent_data:
                        # add the patent data to our collection
                        patents_list.append(patent_data)
                        # increment the successful patents counter
                        count += 1
                        
                        # every 100 patents, print a progress update
                        if count % 100 == 0:
                            print(f"Processed {count} patents (at line {line_num})...")
                
                # reset for the new document
                # start the new document with the current line (containing the XML declaration)
                current_xml = line
                # reset the flag since we're between documents now
                in_patent_doc = False
                # skip to the next line
                continue
            
            # check if this line contains the start of a patent document and we're not already in one
            if not in_patent_doc and patent_start_pattern.search(line):
                # mark that we're now inside a patent document
                in_patent_doc = True
            
            # if we're currently inside a patent document, append this line to the current XML content
            if in_patent_doc:
                current_xml += line
            
            # check if this line contains the end of a patent document and we're currently in one
            if in_patent_doc and patent_end_pattern.search(line):
                # we've reached the end of a complete patent document
                
                # parse the complete patent XML string
                patent_data = parse_patent_xml(current_xml)
                
                # if parsing was successful (didn't return None)
                if patent_data:
                    # add the patent data to our collection
                    patents_list.append(patent_data)
                    # increment the successful patents counter
                    count += 1
                    
                    # every 100 patents, print a progress update
                    if count % 100 == 0:
                        print(f"Processed {count} patents (at line {line_num})...")
                else:
                    # if parsing failed, increment the error counter
                    error_count += 1
                
                # reset variables for the next patent
                # clear the current XML content
                current_xml = ""
                # mark that we're no longer in a patent document
                in_patent_doc = False
                
                # save intermediate results periodically to avoid memory issues since our file is very large
                if count > 0 and count % 1000 == 0:
                    # create a filename for this interim save, including the current count
                    interim_path = f"{os.path.splitext(json_file_path)[0]}_interim_{count}.json"
                    
                    # open the interim file for writing with UTF-8 encoding
                    with open(interim_path, "w", encoding="utf-8") as interim_file:
                        # write the most recent 1000 patents to the interim file
                        # indent=2 creates readable JSON with indentation, ensure_ascii=False preserves non-ASCII characters
                        json.dump(patents_list[-1000:], interim_file, indent=2, ensure_ascii=False)
                    
                    # calculate and report progress information
                    current_time = datetime.now()  # get current time
                    elapsed = current_time - start_time  # calculate elapsed time
                    print(f"Saved {count} patents to {interim_path}. Elapsed time: {elapsed}")
    
    # after processing the entire file, save all collected patent data to the final JSON file
    if patents_list:  # check if we have any successfully processed patents
        # open the output JSON file for writing with UTF-8 encoding
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            # write all patent data to the JSON file
            # indent=2 creates readable JSON with indentation, ensure_ascii=False preserves non-ASCII characters
            json.dump(patents_list, json_file, indent=2, ensure_ascii=False)
        
        # calculate and report final statistics
        end_time = datetime.now()  # get the current time as end time
        elapsed = end_time - start_time  # calculate total elapsed time
        print(f"Data successfully saved as JSON: {json_file_path}")  # report the output file path
        print(f"Total processing time: {elapsed}")  # report the total processing time
        print(f"Processed {count} patents successfully with {error_count} errors")  # report success and error counts
    else:
        # if no patents were processed successfully, print an error message
        print("No patents were processed successfully.")
            
except Exception as e:
    # if any unhandled exception occurs in the main processing block, print an error message
    print(f"An error occurred: {e}")