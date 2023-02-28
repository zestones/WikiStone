function retrieveData() {
    const endpointUrl = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';
    const query =
        `SELECT ?item ?itemLabel ?geoLocation
            WHERE {
                ?item wdt:P9 ?geoLocation.
                SERVICE wikibase:label {
                    bd:serviceParam wikibase:language "en".
                    ?item rdfs:label ?itemLabel.
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

function convertToPositions(data) {
    const positions = [];
    for (const [_, value] of Object.entries(data)) {
        const [lng, lat] = value.geoPoint;
        const position = {
            lat,
            lng,
            popupContent: value.label,
        };
        positions.push(position);
    }
    return positions;
}


function setMap(positions) {
    var map = L.map("map").setView([45.4397, 4.3878], 11);
    var tileLayer = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                '',
            maxZoom: 18,
        }
    );

    tileLayer.addTo(map);
  
    // Loop through the positions and create a marker with a popup for each position
    for (var i = 0; i < positions.length; i++) {
        var position = positions[i];
        var marker = L.marker([position.lat, position.lng]).addTo(map);
        marker.bindPopup(position.popupContent);
    }
}

retrieveData().then(data => {
    const positions = convertToPositions(parseData(data))
    setMap(positions)
});