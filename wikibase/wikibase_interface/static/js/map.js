var map = L.map("map").setView([45.4397, 4.3878], 11);

var tileLayer = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }
);

tileLayer.addTo(map);

// Define a list of geographical positions (latitude, longitude) and associated popup content
var positions = [
    {
        lat: 45.4397,
        lng: 4.3878,
        popupContent: "This is Saint-Etienne",
    },
    {
        lat: 45.7445,
        lng: 4.9442,
        popupContent: "This is Lyon",
    },
];

// Loop through the positions and create a marker with a popup for each position
for (var i = 0; i < positions.length; i++) {
    var position = positions[i];
    var marker = L.marker([position.lat, position.lng]).addTo(map);
    marker.bindPopup(position.popupContent);
}