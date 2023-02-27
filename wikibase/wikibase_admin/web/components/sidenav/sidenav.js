const links = document.querySelectorAll('.sidebar li a');

links.forEach(link => {
    link.addEventListener('click', () => {
        links.forEach(otherLink => otherLink.parentElement.classList.remove('active'));
        link.parentElement.classList.add('active');
    });
});