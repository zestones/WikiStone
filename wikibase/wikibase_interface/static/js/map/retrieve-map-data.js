function retrieveData() {
    const endpointUrl = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';
    const query =
        `SELECT ?item ?itemLabel ?geoLocation WHERE {
            ?item ?p ?geoLocation .
            ?prop wikibase:directClaim ?p ;
                rdfs:label "Location"@en .
            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en" .
                ?item rdfs:label ?itemLabel .
            }
          }          
        `;

    const fullUrl = endpointUrl + '?query=' + encodeURIComponent(query);
    const headers = { 'Accept': 'application/sparql-results+json' };
    // Sends a fetch request to the SPARQL endpoint and returns the response as JSON
    return fetch(fullUrl, { headers }).then(body => body.json());
}

function parseData(rawData) {
    const parsedData = {};

    rawData.results.bindings.forEach(binding => {
        const itemUri = binding.item.value.split('/').pop(); // Get the item ID from the URI
        const label = binding.itemLabel.value;

        // Parse the latitude and longitude from the geoLocation string
        const [latitude, longitude] = binding.geoLocation.value.match(/Point\(([-.\d]+) ([-.\d]+)\)/).slice(1).map(Number);
        parsedData[itemUri] = { label, geoPoint: [latitude, longitude] };
    });

    return parsedData
}

export { retrieveData, parseData };