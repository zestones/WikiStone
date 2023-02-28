function seeMoreResults(results) {
    const resultSection = document.querySelector('.result-section');
    
    // Create form with POST method to action all-results
    const form = document.createElement('form');
    form.classList.add('see-more-form');
    form.setAttribute('method', 'POST');
    form.setAttribute('action', '/all-results');

    // Save results in JSON
    const input = document.createElement('input');
    input.setAttribute('type', 'hidden');
    input.setAttribute('name', 'results');
    input.setAttribute('value', JSON.stringify(results));
    form.appendChild(input);

    // Create the see-more btn
    const seeMoreBtn = document.createElement('button');
    seeMoreBtn.textContent = 'See More';
    seeMoreBtn.classList.add('see-more');
    form.appendChild(seeMoreBtn);

    // Add the form to the DOM
    resultSection.appendChild(form);

    // Add event to the btn (see-more)
    seeMoreBtn.addEventListener('click', () => {
        form.submit();
    });

}

function animateCards() {
    const cards = document.querySelectorAll('.result-section .card.animation-start');
    cards.forEach(card => {
        card.addEventListener('animationend', () => {
            setTimeout(() => {
                card.classList.add('animation-done');
            }, 0.2);
        });
    });
}

export function displaySearch(results) {

    const DISPLAYED_RESULTS = 7;

    // Select the result section element and clear its contents
    const resultSection = document.querySelector('.result-section');
    resultSection.innerHTML = '';

    // If there are no results, display a "no data found" message
    if (Object.keys(results).length === 0) {
        resultSection.innerHTML = '<h2 class="no-result">No data found.</h2>';
    }
    // Otherwise, iterate over the results and create a card for each item
    else {
        let count = 0;
        Object.entries(results).forEach(([_, value]) => {
            // If we've already displayed DISPLAYED_RESULTS cards, exit early
            if (count >= DISPLAYED_RESULTS) return;

            // Create a new card element
            const card = document.createElement('div');
            card.classList.add('card', 'animation-start');

            // Add the item's title to the card
            const title = document.createElement('h2');
            title.textContent = value?.label;
            card.appendChild(title);

            // If the item has a description, add it to the card
            if (value.description) {
                const description = document.createElement('p');
                description.textContent = value?.description;
                card.appendChild(description);
            }

            // Add the card to the result section
            resultSection.appendChild(card);
            count++;
        });
    }

    // If there are more than DISPLAYED_RESULTS results, add a "See More" button to the bottom of the list
    if (Object.keys(results).length > DISPLAYED_RESULTS) {
        seeMoreResults(results);
    }

    // Apply an animation to the cards
    animateCards();
}
