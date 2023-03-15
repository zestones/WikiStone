import { retrieveData, parseData } from "../map/retrieve-map-data.js";
import { setMap, setUserMap, convertToPositions } from "../map/map-config.js";
import { setRadiusMap, displayAllLocation } from "../map/map-slider.js";

let positions;
const map = setMap();

// Retrieve the user's location and display it on the map
navigator.geolocation.getCurrentPosition(function (position) {
    // Get the user's latitude and longitude
    var userPosition = [position.coords.latitude, position.coords.longitude];

    // Retrieve the data and convert it to positions
    retrieveData().then(data => {
        positions = convertToPositions(parseData(data))

        setUserMap(map, userPosition, positions);
        setRadiusMap(map, userPosition, positions);
    });

}, function (error) {
    // Handle the error if geolocation is not supported or if the user denies permission
    console.warn(error);

    // Get the checkbox element
    const displayLocationCheckbox = document.getElementById("displayLocation");

    // Set the checkbox to checked and disabled
    displayLocationCheckbox.checked = true;
    displayLocationCheckbox.disabled = true;

    // Get the slider element
    const slider = document.getElementById("radius-slider");
    slider.disabled = true;

    // Get the Number result element
    const numberResult = document.getElementById("number-results");

    // Retrieve the data and convert it to positions
    retrieveData().then(data => {
        positions = convertToPositions(parseData(data));
        displayAllLocation(map, positions);

        numberResult.innerHTML = (positions.length - 1) + ' ' + 'Results';
    });
});

export { positions, map };