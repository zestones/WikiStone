function displayItemLocation(location) {
    console.log(location)
    var coords = location.split(',');
    const latlng = coords.map(function (coord) {
        return parseFloat(coord.replace(/\[|\]/g, ''));
    });

    // Create the map and add a marker at the item location
    var map = L.map('map').setView(latlng, 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '',
        maxZoom: 18
    }).addTo(map);
    L.marker(latlng).addTo(map);
}