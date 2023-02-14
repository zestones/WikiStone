const cards = document.querySelectorAll('.result-section .card');

cards.forEach(card => {
    card.addEventListener('animationend', () => {
        card.classList.add('animation-done');
    });
});