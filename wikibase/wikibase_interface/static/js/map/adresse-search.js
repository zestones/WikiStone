import { positions, map } from '../map/map.js';
import { setUserMap } from './map-config.js';
import { setRadiusMap } from './map-slider.js';


const API_KEY = 'ck2OXUAJsF0iz999XGQ62jyXo8AXOVp7';
const searchForm = document.querySelector('#search-container');

searchForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const searchInput = document.querySelector('#search-input');
    const address = searchInput.value;

    fetch(`https://www.mapquestapi.com/geocoding/v1/address?key=${API_KEY}&location=${address}`)
        .then(response => response.json())
        .then(data => {
            const latitude = data.results[0].locations[0].latLng.lat;
            const longitude = data.results[0].locations[0].latLng.lng;
            const userPosition = [latitude, longitude]; 
            
            map.setView(userPosition, 11);
            setUserMap(map, userPosition, positions);
            setRadiusMap(map, userPosition, positions);
        })
        .catch(error => console.error(error));
});

export { API_KEY };