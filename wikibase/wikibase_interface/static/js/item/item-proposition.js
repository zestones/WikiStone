import SPARQLQueryDispatcher from "../search/SPARQLQueryDispatcher.js";

function searchNearbyMonuments(coordinates) {
    const position = "Point(" + coordinates.reverse().join(" ") + ")";

    const sparqlQuery = `
        SELECT ?item ?itemLabel ?distance WHERE {
            SERVICE wikibase:around {
                ?item wdt:P9 ?location.
                bd:serviceParam wikibase:center "${position}"^^geo:wktLiteral;
                wikibase:radius "50";
                wikibase:distance ?distance.
            }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            FILTER (?distance > 0)
        }
        ORDER BY (?distance)
        LIMIT 12`
        ;

    return sparqlQuery;
}

function displayResult(parsedData) {

    let html = '';
    for (const item in parsedData) {
        let distance = parsedData[item].distance;

        // convert distance to a number
        distance = parseFloat(distance);
        if (distance < 1) distance = (distance * 1000).toFixed(0) + ' m';
        else distance = distance.toFixed(2) + ' km';

        html += `
            <div class="item-card-proposition">
                <h4 onclick="window.location='/result?id=${item}'">${parsedData[item].label}</h4>
                <p><strong>Distance: </strong>${distance}</p>
            </div>
        `;
    }


    // Insérer le contenu HTML dans la section
    section.innerHTML = `
        <div class="carousel">
            ${html}
        </div>
        <button class="carousel-prev"></button>
        <button class="carousel-next"></button>
    `;

    // Initialize Slick.js carousel
    $('.carousel').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        prevArrow: $('.carousel-prev'),
        nextArrow: $('.carousel-next'),
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }
        ]
    });
}


// Get the map element
const mapElement = document.getElementById('map');
const location = mapElement.getAttribute('data-location');
const section = document.querySelector('.item-proposition');

const sparqlQuery = searchNearbyMonuments(JSON.parse(location));

const queryDispatcher = new SPARQLQueryDispatcher();
queryDispatcher.query(sparqlQuery)
    .then((data) => {
        const parsedData = queryDispatcher.parse(data);
        const sortedKeys = Object.keys(parsedData).sort((a, b) => {
            const distanceA = parseFloat(parsedData[a].distance);
            const distanceB = parseFloat(parsedData[b].distance);
            return distanceA - distanceB;
        });

        const sortedData = {};
        sortedKeys.forEach((key) => {
            sortedData[key] = parsedData[key];
        });

        displayResult(sortedData);
    })
    .catch((error) => {
        console.log("error" + error)
    });
