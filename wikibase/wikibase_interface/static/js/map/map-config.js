import { setRadiusMap } from "../map/map-slider.js";
import { API_KEY } from "./adresse-search.js";

function convertToPositions(data) {
    const positions = [];
    for (const [id, value] of Object.entries(data)) {
        const [lng, lat] = value.geoPoint;
        const position = {
            lat,
            lng,
            popupContent: `<a class='popup-link' href='/result?id=${id}'>${value.label}</a> `,
        };
        positions.push(position);
    }
    return positions;
}

function setMap() {
    const saintEtienne = [45.4397, 4.3878];
    const map = L.map("map").setView(saintEtienne, 11);
    const tileLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "",
        maxZoom: 18,
    });

    tileLayer.addTo(map);

    // Initialize place search with options
    placeSearch({
        key: API_KEY,
        container: document.querySelector("#search-input"),
        useDeviceLocation: true,
        collection: ["poi", "airport", "address", "adminArea"],
    });

    return map;
}

let userMarker;
let changePositionBtnListener;

function setUserMap(map, userPosition, positions) {
    // Create a red icon for the user marker
    const userIcon = L.icon({
        iconUrl:
            "https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
    });

    if (userMarker) map.removeLayer(userMarker);

    // Create a marker for the user location with the custom icon
    userMarker = L.marker(userPosition, { icon: userIcon }).addTo(map);
    userMarker.bindPopup("Your location");

    if (changePositionBtnListener) {
        changePositionBtn.removeEventListener("click", changePositionBtnListener);
    }
    changePositionBtnListener = function (e) {
        e.stopPropagation();

        if (isChangingPosition) {
            // Remove the click event listener from the map
            map.off("click");
            isChangingPosition = false;
            changePositionBtn.innerText = "Change Position";
            changePositionBtn.classList.remove("change-position");
        } else {
            // Add the click event listener to the map
            map.on("click", function (e) {
                userMarker.setLatLng(e.latlng);
                setRadiusMap(map, [e.latlng.lat, e.latlng.lng], positions);
            });
            isChangingPosition = true;
            changePositionBtn.innerText = "Stop Changing";
            changePositionBtn.classList.add("change-position");
        }
    };
    changePositionBtn.addEventListener("click", changePositionBtnListener);
}

const changePositionBtn = document.getElementById("change-position-btn");
let isChangingPosition = false;

const mapContainer = document.getElementById("map");

// Add a mousemove event listener to the map container
mapContainer.addEventListener("mousemove", function (e) {
    if (isChangingPosition) {
        // Change the cursor to the marker icon
        mapContainer.style.cursor =
            "url('https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png') 12 41, pointer";
    } else {
        // Change the cursor back to the default cursor
        mapContainer.style.cursor = "grab";
    }
});

const searchContainer = document.querySelector('.search-container');
const searchInput = document.querySelector('#search-input');

// Add a mousedown event listener to the search container to prevent the event from propagating to the map
searchContainer.addEventListener('mousedown', function (e) {
    // Check if the target element of the event is the input element or the dropdown menu
    if (
        e.target === searchInput ||
        e.target.parentNode.id === 'mq-place-search-listbox-0'
    ) {
        // Stop the event propagation
        e.stopPropagation();
        // Allow the default behavior of the mousedown event to happen
        return true;
    } else {
        // Stop the event propagation
        e.stopPropagation();
        return false;
    }
});


export { setMap, setUserMap, convertToPositions };
