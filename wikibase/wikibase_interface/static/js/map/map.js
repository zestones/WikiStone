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

function createCircleRadius(radius, userPosition) {
    return L.circle(userPosition, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1,
        radius: radius
    });
}

function userLocation(map, userPosition) {
    // Save a reference to the previously drawn circle
    let circle;

    // Get the slider element
    const slider = document.getElementById("radius-slider");

    // Get the value element
    const value = document.getElementById("radius-value");

    // Update the value element with the initial value
    value.innerHTML = (slider.value / 1000).toFixed(1) + " km";

    circle = createCircleRadius(slider.value, userPosition).addTo(map);

    // Update the value element when the slider value changes
    slider.addEventListener("input", function () {
        const radius = this.value;
        value.innerHTML = (radius / 1000).toFixed(1) + " km";;

        // Remove the previously drawn circle, if it exists
        if (circle) {
            map.removeLayer(circle);
        }

        // Create a new circle and add it to the map
        circle = createCircleRadius(radius, userPosition).addTo(map);
    });
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

    // Create a red icon for the user marker
    const userIcon = L.icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    // Create a marker for the user location with the custom icon
    const userMarker = L.marker(userPosition, { icon: userIcon }).addTo(map);
    userMarker.bindPopup("Your location");

    userLocation(map, userPosition);

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