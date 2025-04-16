document.addEventListener('DOMContentLoaded', function() { // wait for the DOM to be fully loaded before executing anything
    // all the references to the DOM elements we need to interact with for now
    const searchButton = document.getElementById('search-button'); // button to trigger the search
    const searchForm = document.getElementById('search-form')
    const resultsContainer = document.getElementById('results'); // container where the search results will be displayed
    const loadingIndicator = document.getElementById('loading'); // loading message that appears during search
    const tooltipIcon = document.getElementById('tooltip-icon'); // variables for the search tool tip
    const tooltipText = document.querySelector('.tooltip-text'); // - text can be changed later

     // Form submission handler
     searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch(new FormData(this));
    });

    // main search function that will be triggered when the user clicks search
    // async function because we need to 'await' the fetch request
    async function performSearch(formData) {

        // convert FormData to object
        const searchParams = Object.fromEntries(formData);
        
        // validate at least one field has content
        const hasQuery = Object.values(searchParams).some(value => value && value.toString().trim() !== '');
        
        if (!hasQuery) {
            // if no fields are filled, show an error message
            resultsContainer.innerHTML = '<p class="no-results">Please enter a search term.</p>';
            return; // exit the function early
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
                body: JSON.stringify({searchParams}) // convert the search term to JSON
            });
            
            if (!response.ok) { // check if the HTTP request was successful (status code: 200-299)
                // if it was not successful, throw an error with the HTTP status code
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            // parse the response from the server as JSON
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






    tooltipIcon.addEventListener('mouseenter', function() {
        tooltipText.style.display = 'block';
        tooltipText.style.opacity = '1';
    })

    tooltipIcon.addEventListener('mouseleave', function() {
        tooltipText.style.display = 'none';
        tooltipText.style.opacity = '0';
    })
});