import { retrieveData, parseData } from "../map/retrieve-map-data.js";
import { setMap, setUserMap, convertToPositions } from "../map/map-config.js";
import { setRadiusMap } from "../map/map-slider.js";


// Retrieve the user's location and display it on the map
navigator.geolocation.getCurrentPosition(function (position) {
    // Get the user's latitude and longitude
    var userPosition = [position.coords.latitude, position.coords.longitude];

    // Retrieve the data and convert it to positions
    retrieveData().then(data => {
        const positions = convertToPositions(parseData(data))

        // Display the map with the user's position and the retrieved positions
        const map = setMap();

        setUserMap(map, userPosition);
        setRadiusMap(map, userPosition, positions);
    });

}, function (error) {
    // Handle the error if geolocation is not supported or if the user denies permission
    console.log(error);
});