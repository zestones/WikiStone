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


function setMap() {

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

    return map;
}


function setUserMap(map, userPosition) {
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
}

export { setMap, setUserMap, convertToPositions };