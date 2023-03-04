class SPARQLQueryDispatcher {

    constructor() {
        this.endpoint = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';;
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
            const id = binding?.id?.value.split("/").pop();
            const label = binding?.label?.value;
            const description = binding?.description?.value;
            const type = binding?.type?.value.split("#").pop();
            items[id] = { label, description, type };
        });

        return items;
    }
}

function searchAllProrperties() {
    const sparqlQuery =  `SELECT ?id ?label ?description ?type
        WHERE { 
            ?property a wikibase:Property ;
                wikibase:propertyType ?type ;
                wikibase:directClaim ?id ;
                rdfs:label ?label ;
                schema:description ?description .
            FILTER(LANG(?label) = "" || LANG(?label) = "en")
            FILTER(LANG(?description) = "" || LANG(?description) = "en")
        }
    `;

    return sparqlQuery;
}

const sparqlQuery = searchAllProrperties();

const queryDispatcher = new SPARQLQueryDispatcher();
queryDispatcher.query(sparqlQuery)
    .then((data) => {
        console.log(data)
        console.log(queryDispatcher.parse(data))
    })
    .catch((error) => {
        console.log('error' + error)
    });