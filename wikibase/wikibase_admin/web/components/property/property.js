class SPARQLQueryDispatcher {

    constructor() {
        this.endpoint = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';;
    }

    query(sparqlQuery) {
        const fullUrl = this.endpoint + '?query=' + encodeURIComponent(sparqlQuery);
        const headers = { 'Accept': 'application/sparql-results+json' };
        // Sends a fetch request to the SPARQL endpoint and returns the response as JSON
        return fetch(fullUrl, { headers }).then(body => body.json());
    }

    parse(data) {
        const items = {};

        // If there are no results, return an empty object
        if (data.results.bindings.length === 0) return items;

        // Create an object with the results
        data.results.bindings.forEach((binding) => {
            const id = binding?.id?.value.split("/").pop();
            const label = binding?.label?.value;
            const description = binding?.description?.value;
            const type = binding?.type?.value.split("#").pop();
            items[id] = { label, description, type };
        });

        return items;
    }
}

function searchAllProrperties() {
    const sparqlQuery = `SELECT ?id ?label ?description ?type
        WHERE { 
            ?property a wikibase:Property ;
                wikibase:propertyType ?type ;
                wikibase:directClaim ?id ;
                rdfs:label ?label ;
                schema:description ?description .
            FILTER(LANG(?label) = "" || LANG(?label) = "en")
            FILTER(LANG(?description) = "" || LANG(?description) = "en")
        }
    `;

    return sparqlQuery;
}

document.addEventListener('DOMContentLoaded', () => {
    const sparqlQuery = searchAllProrperties();
    const queryDispatcher = new SPARQLQueryDispatcher();
    queryDispatcher.query(sparqlQuery)
        .then((data) => {
            const parsedData = queryDispatcher.parse(data);
            setTimeout(() => displayProperties(parsedData), 100);
        })
        .catch((error) => {
            console.log('error' + error);
        });
});


function displayProperties(properties) {
    const propertyNames = Object.keys(properties);
    const propertyList = document.querySelector('#property-names');

    if (propertyNames.length === 0) {
        console.warn('No properties found.');
        return;
    }

    const firstPropertyName = propertyNames[0];

    propertyNames.forEach(name => {
        const li = document.createElement('li');
        li.textContent = name + ` (${properties[name].label})`;
        li.addEventListener('click', () => {
            // remove active class from any existing active list item
            const activeItem = propertyList.querySelector('.active');
            if (activeItem) {
                activeItem.classList.remove('active');
            }
            // add active class to the clicked item
            li.classList.add('active');
            displayPropertyDetails(properties, name);
        });

        propertyList.appendChild(li);
    });

    // add active class to the first item
    propertyList.querySelector(`li:first-child`).classList.add('active');
    displayPropertyDetails(properties, firstPropertyName);
}


function displayPropertyDetails(properties, name) {
    const property = properties[name];

    const propertyTitle = document.querySelector('#property-title');
    propertyTitle.textContent = property.label;

    const propertyDescription = document.querySelector('#property-description');
    propertyDescription.textContent = property.description;

    const propertyType = document.querySelector('#property-type');
    propertyType.textContent = `Type: ${property.type}`;

    const propertyDetails = document.querySelector('#property-details');
    propertyDetails.style.display = 'block';

    // Check if a modify button already exists
    const existingModifyButton = document.querySelector('.btn-modify');
    if (existingModifyButton) {
        existingModifyButton.remove();
    }

    const modifyButton = document.createElement('button');
    modifyButton.innerHTML = '<i class="fas fa-edit"></i>Modify';
    modifyButton.classList.add('btn-modify');
    modifyButton.onclick = () => {
        console.log(`Modify button clicked for property with ID: ${name}`);
        // Add your code to modify the property here
        const newLabel = propertyTitle.textContent;
        const newDescription = propertyDescription.textContent;

        // Call a function to update the property with the new details
        updateProperty(name, newLabel, newDescription);
        // Update the fields
        propertyTitle.textContent = newLabel;
        propertyDescription.textContent = newDescription;
        
        // Update the data Object
        properties[name].label = newLabel;
        properties[name].description = newDescription;

        // Update the label
        const propertyList = document.querySelector('#property-names');
        let activeItem = propertyList.querySelector('.active');
        activeItem.textContent = name + ` (${properties[name].label})`;
    };
    propertyDetails.appendChild(modifyButton);
}


async function updateProperty(id, label, description) {
    await eel.updateProperty(id, label, description)();
}