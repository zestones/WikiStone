export default class SPARQLQueryDispatcher {
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
            const distance = binding?.distance?.value;
            items[id] = { label, description, distance };
        });

        return items;
    }
}