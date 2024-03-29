function createCircleRadius(radius, userPosition) {
    return L.circle(userPosition, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.1,
        radius: radius
    });
}

// Create an object to store all the marker objects
const markers = {};

function updateVisibleLocation(map, positions, userLatLng) {
    // Filter the positions based on their distance from the user's location and the radius
    const filteredPositions = positions.filter(position => {
        const positionLatLng = L.latLng(position.lat, position.lng);
        const distance = userLatLng.distanceTo(positionLatLng);
        return distance <= slider.value;
    });

    // Loop through the filtered positions and create a marker with a popup for each position
    for (var i = 0; i < filteredPositions.length; i++) {
        var position = filteredPositions[i];
        // Generate a unique ID for the marker
        const markerId = position.lat + '&' + position.lng;

        // Check if the marker has already been added to the map
        if (!markers[markerId]) {
            var marker = L.marker([position.lat, position.lng]).addTo(map);
            marker.bindPopup(position.popupContent);
            // Add the marker's ID to the object of markers
            markers[markerId] = marker;
        }
    }

    // Remove markers that are not within the radius
    for (const markerId in markers) {
        const marker = markers[markerId];
        const latLng = marker._latlng;
        const isMarkerInRadius = filteredPositions.some(position => {
            return position.lat === latLng.lat && position.lng === latLng.lng;
        });
        if (!isMarkerInRadius) {
            map.removeLayer(marker);
            delete markers[markerId];
        }
    }
}

function displayAllLocation(map, positions) {

    // Loop through the positions and create a marker with a popup for each position
    for (var i = 0; i < positions.length; i++) {
        var position = positions[i];
        // Generate a unique ID for the marker
        const markerId = position.lat + '&' + position.lng;

        if (!markers[markerId]) {
            var marker = L.marker([position.lat, position.lng]).addTo(map);
            marker.bindPopup(position.popupContent);

            // Add the marker's ID to the object of markers
            markers[markerId] = marker;
        }
    }
}

// Save a reference
let circle;
let sliderInputListener;
let displayLocationCheckboxListener;

function setRadiusMap(map, userPosition, positions) {
    // Remove the previously drawn circle, if it exists
    if (circle) map.removeLayer(circle);
    
    // Update the value element with the initial value
    value.innerHTML = (slider.value / 1000).toFixed(1) + " km";
    circle = createCircleRadius(slider.value, userPosition).addTo(map);

    const userLatLng = L.latLng(userPosition);
    updateVisibleLocation(map, positions, userLatLng);
    
    numberResult.innerHTML = Object.keys(markers).length + ' ' + 'Results';

    // Update the slider input event listener
    if (sliderInputListener) {
        slider.removeEventListener("input", sliderInputListener);
    }
    sliderInputListener = function () {
        const radius = this.value;
        value.innerHTML = (radius / 1000).toFixed(1) + " km";

        // Remove the previously drawn circle, if it exists
        if (circle) map.removeLayer(circle);

        // Create a new circle and add it to the map
        circle = createCircleRadius(radius, userPosition).addTo(map);
        if (!displayLocationCheckbox.checked) {
            updateVisibleLocation(map, positions, userLatLng);
        }

        numberResult.innerHTML = Object.keys(markers).length + ' ' + 'Results';
    };
    slider.addEventListener("input", sliderInputListener);

    // Update the display location checkbox change event listener
    if (displayLocationCheckboxListener) {
        displayLocationCheckbox.removeEventListener("change", displayLocationCheckboxListener);
    }
    displayLocationCheckboxListener = function () {
        if (this.checked) {
            displayAllLocation(map, positions, userLatLng);
        } else {
            // Checkbox is not checked, hide all positions
            updateVisibleLocation(map, positions, userLatLng);
        }
        numberResult.innerHTML = Object.keys(markers).length + ' ' + 'Results';
    };
    displayLocationCheckbox.addEventListener("change", displayLocationCheckboxListener);
}

// Get the slider element
const slider = document.getElementById("radius-slider");
const value = document.getElementById("radius-value");

// Get the checkbox element
const displayLocationCheckbox = document.getElementById("displayLocation");

// Get the Number result element
const numberResult = document.getElementById("number-results");

export { setRadiusMap, displayAllLocation };