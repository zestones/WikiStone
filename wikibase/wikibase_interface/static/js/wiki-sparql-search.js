class SPARQLQueryDispatcher {
    constructor() {
        this.endpoint = 'http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql';
    }

    construct(formData) {
        let sparqlQuery = `SELECT ?item ?itemLabel ?itemDescription WHERE {`;
        const conditions = [];

        if (formData.city) conditions.push(`?item wdt:P3 "${formData.city}".`);
        if (formData.postalCode) conditions.push(`?item wdt:P4 "${formData.postalCode}".`);
        if (formData.region) conditions.push(`?item wdt:P6 "${formData.region}".`);

        if (formData.query) {
            sparqlQuery += `?item rdfs:label ?itemLabel.
            FILTER(REGEX(?itemLabel, "${formData.query}", "i")).`;
        }

        sparqlQuery += conditions.join(' ') + `
            SERVICE wikibase:label {
                bd:serviceParam wikibase:language "en".
            }
        }
        LIMIT 50
        `;

        return sparqlQuery;
    }

    query(sparqlQuery) {
        const fullUrl = this.endpoint + '?query=' + encodeURIComponent(sparqlQuery);
        const headers = { 'Accept': 'application/sparql-results+json' };

        return fetch(fullUrl, { headers }).then(body => body.json());
    }

    parse(data) {
        const items = {};

        if (data.results.bindings.length === 0)
            return items;

        data.results.bindings.forEach((binding) => {
            const id = binding?.item?.value.split("/").pop();
            const label = binding?.itemLabel?.value;
            const description = binding?.itemDescription?.value;
            items[id] = { label, description };
        });

        return items;
    }
}

function getFormData() {
    const formData = new FormData(form);
    return {
        query: formData.get('query'),
        city: formData.get('city'),
        postalCode: formData.get('postal-code'),
        region: formData.get('region')
    };
}

function displaySearch(results) {
    const resultSection = document.querySelector('.result-section');
    resultSection.innerHTML = '';

    if (Object.keys(results).length === 0) resultSection.innerHTML = '<h2 class="no-result">No data found.</h2>';
    else {
        let count = 0;
        Object.entries(results).forEach(([_, value]) => {
            if (count >= 7) return;

            const card = document.createElement('div');
            card.classList.add('card', 'animation-start');

            const title = document.createElement('h2');
            title.textContent = value?.label;
            card.appendChild(title);

            if (value.description) {
                const description = document.createElement('p');
                description.textContent = value?.description;
                card.appendChild(description);
            }

            resultSection.appendChild(card);
            count++;
        });

        if (Object.keys(results).length > 7) {
            const seeMoreBtn = document.createElement('button');
            seeMoreBtn.textContent = 'See More';
            seeMoreBtn.classList.add('see-more');
            resultSection.appendChild(seeMoreBtn);
        }
    }

    const cards = document.querySelectorAll('.result-section .card.animation-start');
    cards.forEach(card => {
        card.addEventListener('animationend', () => {
            setTimeout(() => {
                card.classList.add('animation-done');
            }, 0.2);
        });
    });
}


function validateForm(formData) {

    if (!formData.query && !formData.city && !formData.postalCode && !formData.region) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerHTML = 'Please provide at least one search criteria.';
        errorMessage.style.display = 'block';
        return false;
    }

    const errorMessage = document.getElementById('error-message');
    errorMessage.style.display = 'none';

    return true;
}

// Get the form element
const form = document.querySelector('form');

// Add an event listener for when the form is submitted
form.addEventListener('submit', event => {
    // Prevent the form from submitting normally
    event.preventDefault();

    const queryDispatcher = new SPARQLQueryDispatcher();

    // Get the form data
    formData = getFormData()
    if (!validateForm(formData)) return;

    // clear the search input fields
    form.reset(); 

    // Construct the SPARQL query
    sparqlQuery = queryDispatcher.construct(formData);

    // Fetch and Parse the data
    queryDispatcher.query(sparqlQuery)
        .then(data => {
            // Collapse the search options
            searchOptions.classList.remove('visible');
            container.classList.remove('expanded');

            // Pass the parsed data to the displaySearch function
            displaySearch(queryDispatcher.parse(data));
        })
        .catch(error => {
            console.error(error);
            // Display an error message if there was an error
            resultSection.innerHTML = '<h2>An error occurred while fetching the data.</h2>';
        });
});
