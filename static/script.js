document.addEventListener('DOMContentLoaded', function() { // wait for the DOM to be fully loaded before executing anything
    // all the references to the DOM elements we need to interact with for now
    const searchInput = document.getElementById('search-input'); // text input field
    const searchButton = document.getElementById('search-button'); // button to trigger the search
    const resultsContainer = document.getElementById('results'); // container where the search results will be displayed
    const loadingIndicator = document.getElementById('loading'); // loading message that appears during search
    
    // main search function that will be triggered when the user clicks search
    // async function because we're using 'await' for the fetch request
    async function performSearch() {
        const searchTerm = searchInput.value.trim(); // get the user input and trim whitespace
        
        if (searchTerm === '') { // validate that the user actually entered something
            // if no search term is provided, show a messgage and exit function
            resultsContainer.innerHTML = '<p class="no-results">Please enter a search term.</p>';
            return;
        }
        
        // Show loading indicator to indicate search in progress
        loadingIndicator.style.display = 'block';
        // clear any previous results
        resultsContainer.innerHTML = '';
        
        try {
            // make asynchronous POST request to the server's /search endpoint
            // endpoint is defined in app.py - handles database query
            const response = await fetch('/search', {
                method: 'POST', // using POST method to send the search query
                headers: {
                    'Content-Type': 'application/json' // tell the server we are sending JSON data
                },
                body: JSON.stringify({ query: searchTerm }) // convert the search term to JSON
            });
            
            if (!response.ok) { // check if the HTTP request was successful (status code: 200-299)
                // if it was not successful, throw an error with the HTTP status code
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            // parse the JSON response from the server
            // this contains the patent search result from the database
            const data = await response.json();
            
            // hide loading indicator since we have received the results
            loadingIndicator.style.display = 'none';
            
            // check if any patents were found that match the search query
            if (data.length === 0) {
                // if no patents found, display a message
                resultsContainer.innerHTML = '<p class="no-results">No patents found matching your search.</p>';
            } else {
                // if patents were found, create HTML to display them
                let resultsHTML = '';
                
                // loop through each patent in the results and build the HTML for each one
                data.forEach(patent => {
                    resultsHTML += `
                        <div class="patent-item">
                            <div class="patent-title">${patent.title}</div>
                            <div class="patent-details">
                                <strong>ID:</strong> ${patent.id} | 
                                <strong>Author(s):</strong> ${patent.authors} | 
                                <strong>Filed:</strong> ${patent.date}
                            </div>
                            <div class="patent-description">${patent.description}</div>
                        </div>
                    `;
                });
                
                // insert all the patent HTML into the result container
                resultsContainer.innerHTML = resultsHTML;
            }
        } catch (error) {
            // for if any errors occur during the fetch operation or result processing

            // hide loading indicator
            loadingIndicator.style.display = 'none';
            
            // display error message
            resultsContainer.innerHTML = `<p class="no-results">Error: ${error.message}</p>`;
            
            // log the full error to the console for debugging
            console.error('Search error:', error);
        }
    }
    

    // event listeners to triger the search functon
    searchButton.addEventListener('click', performSearch); // run performSearch when the searchButton is clicked
    
    // also perform the search when the user presses Enter while in the search input field
    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
});