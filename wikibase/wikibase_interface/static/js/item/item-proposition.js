import SPARQLQueryDispatcher from "../search/SPARQLQueryDispatcher.js";

function searchNearbyMonuments(coordinates) {
    const position = "Point(" + coordinates.reverse().join(" ") + ")";
    console.log(position);
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
        LIMIT 3`
        ;

    return sparqlQuery;
}

function displayResult(parsedData) {
    console.log(parsedData)
    // Générer le contenu HTML à partir des données
    let html = '';

    for (const item in parsedData) {
        html += `
                <div class="item-card-proposition">
                    <h4 onclick="window.location='/result?id=${item}'">${parsedData[item].label}</h4>
                    <p>Distance: ${parsedData[item].distance} km</p>
                `;
        if (parsedData[item].description) {
            html += `
                    <p>${parsedData[item].description}</p>
                    </div>
                `;
        }
        else html += '</div>';
    }

    // Insérer le contenu HTML dans la section
    section.innerHTML = html;
}

// Get the map element
const mapElement = document.getElementById('map');
const location = mapElement.getAttribute('data-location');
const section = document.querySelector('.item-proposition');

const sparqlQuery = searchNearbyMonuments(JSON.parse(location));

const queryDispatcher = new SPARQLQueryDispatcher();
queryDispatcher.query(sparqlQuery)
    .then((data) => {
        displayResult(queryDispatcher.parse(data));
    })
    .catch((error) => {
        console.log("error" + error)
    })
