class SPARQLQueryDispatcher {
    constructor() {
        this.endpoint = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';
    }

    construct(formData) {
        const query = formData.get('query');
        const city = formData.get('city');
        const postalCode = formData.get('postal-code');
        const region = formData.get('region');


        let sparqlQuery = `SELECT ?item ?itemLabel ?itemDescription WHERE {`;
        const conditions = [];

        if (city) conditions.push(`?item wdt:P3 "${city}".`);
        if (postalCode) conditions.push(`?item wdt:P4 "${postalCode}".`);
        if (region) conditions.push(`?item wdt:P6 "${region}".`);

        if (query) {
            sparqlQuery += `?item rdfs:label ?itemLabel.
            FILTER(REGEX(?itemLabel, "${query}", "i")).`;
        }

        sparqlQuery += conditions.join(' ') + `
            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en".
            }
        }`;

        return sparqlQuery;
    }

    query(sparqlQuery) {
        const fullUrl = this.endpoint + '?query=' + encodeURIComponent(sparqlQuery);
        const headers = { 'Accept': 'application/sparql-results+json' };

        return fetch(fullUrl, { headers }).then(body => body.json());
    }

    parse(data) {
        const items = {};

        data.results.bindings.forEach((binding) => {
            const id = binding?.item?.value.split("/").pop();
            const label = binding?.itemLabel?.value;
            const description = binding?.itemDescription?.value;
            items[id] = { label, description };
        });

        console.log(items)
    }
}

// Get the form element
const form = document.querySelector('form');

// Add an event listener for when the form is submitted
form.addEventListener('submit', event => {
    // Prevent the form from submitting normally
    event.preventDefault();

    const queryDispatcher = new SPARQLQueryDispatcher();

    // Get the form data
    const formData = new FormData(form);
    
    // Construct the SPARQL query
    sparqlQuery = queryDispatcher.construct(formData);
    // Fetch and Parse the data
    queryDispatcher.query(sparqlQuery).then(queryDispatcher.parse);
});