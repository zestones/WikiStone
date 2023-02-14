const cards = document.querySelectorAll('.result-section .card.animation-start');

cards.forEach(card => {
    card.addEventListener('animationend', () => {
        card.classList.add('animation-done');
    });
});