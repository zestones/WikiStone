function loadHomeContent() {
    fetch('components/home.html')
        .then(response => response.text())
        .then(data => {
            const home = document.getElementById('home');
            home.innerHTML = data;
        })
        .catch(error => console.error(error));
}

const homeTab = document.querySelector('#home-tab');

homeTab.addEventListener('click', () => {
    loadHomeContent();
});
