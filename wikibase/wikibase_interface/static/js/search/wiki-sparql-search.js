import { displaySearch } from "../search/display-search-results.js";
import { validateForm } from "../search/validate-form.js";
import SPARQLQueryDispatcher from "./SPARQLQueryDispatcher.js";

// Extract the User input of the Form
function getFormData(form) {
    const formData = new FormData(form);
    return {
        query: formData.get('query'),
        city: formData.get('city'),
        postalCode: formData.get('postal-code'),
        region: formData.get('region')
    };
}

// Get the form element
const form = document.querySelector('form');

// Add an event listener for when the form is submitted
form.addEventListener('submit', event => {
    // Prevent the form from submitting normally
    event.preventDefault();

    const queryDispatcher = new SPARQLQueryDispatcher();

    // Get the form data
    const formData = getFormData(form)
    if (!validateForm(formData)) return;

    // clear the search input fields
    form.reset();

    // Construct the SPARQL query
    const sparqlQuery = queryDispatcher.construct(formData);

    // Fetch and Parse the data
    queryDispatcher.query(sparqlQuery)
        .then(data => {
            // Collapse the search options
            searchOptions.classList.remove('visible');
            container.classList.remove('expanded');

            // Pass the parsed data to the displaySearch function
            displaySearch(queryDispatcher.parse(data));
        })
        .catch(error => {
            console.error(error);
            // Display an error message if there was an error
            const resultSection = document.querySelector('.result-section');
            resultSection.innerHTML = `<h2 class='fetch-error'>An error occurred while fetching the data.</h2>`;
        });
});
