import { displaySearch } from "../search/display-search-results.js";
import { validateForm } from "../search/validate-form.js";

class SPARQLQueryDispatcher {
    constructor() {
        // Sets the SPARQL endpoint URL
        this.endpoint = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';
    }

    // Constructs the full SPARQL query with the conditions and limits the results to 50
    construct(formData) {
        let sparqlQuery = `SELECT ?item ?itemLabel ?itemDescription WHERE {`;
        const conditions = [];

        if (formData.city) conditions.push(`?item wdt:P3 "${formData.city}".`);
        if (formData.postalCode) conditions.push(`?item wdt:P4 "${formData.postalCode}".`);
        if (formData.region) conditions.push(`?item wdt:P6 "${formData.region}".`);

        if (formData.query) {
            sparqlQuery += `?item rdfs:label ?itemLabel.
            FILTER(REGEX(?itemLabel, "${formData.query}", "i")).`;
        }

        sparqlQuery += conditions.join(' ') + `
            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en".
            }
        }
        LIMIT 50
        `;

        return sparqlQuery;
    }

    query(sparqlQuery) {
        const fullUrl = this.endpoint + '?query=' + encodeURIComponent(sparqlQuery);
        const headers = { 'Accept': 'application/sparql-results+json' };
        // Sends a fetch request to the SPARQL endpoint and returns the response as JSON
        return fetch(fullUrl, { headers }).then(body => body.json());
    }

    parse(data) {
        const items = {};

        // If there are no results, return an empty object
        if (data.results.bindings.length === 0) return items;

        // Create an object with the results
        data.results.bindings.forEach((binding) => {
            const id = binding?.item?.value.split("/").pop();
            const label = binding?.itemLabel?.value;
            const description = binding?.itemDescription?.value;
            items[id] = { label, description };
        });

        return items;
    }
}

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
