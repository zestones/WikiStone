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


function setMap(positions, userPosition) {

    const saintEtienne = [45.4397, 4.3878];
    var map = L.map("map").setView(saintEtienne, 11);
    var tileLayer = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                '',
            maxZoom: 18,
        }
    );

    tileLayer.addTo(map);

    // Define the SVG code
    const svgCode = '<svg fill="#ff0000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-39.57 -39.57 474.85 474.85" xml:space="preserve" stroke="#ff0000" transform="rotate(0)matrix(1, 0, 0, 1, 0, 0)" stroke-width="0.0039571"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M197.849,0C122.131,0,60.531,61.609,60.531,137.329c0,72.887,124.591,243.177,129.896,250.388l4.951,6.738 c0.579,0.792,1.501,1.255,2.471,1.255c0.985,0,1.901-0.463,2.486-1.255l4.948-6.738c5.308-7.211,129.896-177.501,129.896-250.388 C335.179,61.609,273.569,0,197.849,0z M197.849,88.138c27.13,0,49.191,22.062,49.191,49.191c0,27.115-22.062,49.191-49.191,49.191 c-27.114,0-49.191-22.076-49.191-49.191C148.658,110.2,170.734,88.138,197.849,88.138z"></path> </g> </g></svg>';

    // Define the custom icon using the SVG code
    const customIcon = L.icon({
        iconUrl: 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgCode),
        iconSize: [40, 40], // Adjust the size of the icon as needed
        iconAnchor: [20, 0], // Adjust the anchor point of the icon as needed
    });

    // Create a marker using the custom icon
    const userMarker = L.marker(userPosition, { icon: customIcon }).addTo(map);
    userMarker.bindPopup("<div class='popup'><p>Your location</p></div>");


    // Loop through the positions and create a marker with a popup for each position
    for (var i = 0; i < positions.length; i++) {
        var position = positions[i];
        var marker = L.marker([position.lat, position.lng]).addTo(map);
        marker.bindPopup(position.popupContent);
    }
}

// Retrieve the user's location and display it on the map
navigator.geolocation.getCurrentPosition(function (position) {
    // Get the user's latitude and longitude
    var userPosition = [position.coords.latitude, position.coords.longitude];

    // Retrieve the data and convert it to positions
    retrieveData().then(data => {
        const positions = convertToPositions(parseData(data))

        // Display the map with the user's position and the retrieved positions
        setMap(positions, userPosition);
    });
}, function (error) {
    // Handle the error if geolocation is not supported or if the user denies permission
    console.log(error);
});