function loadSourceContent() {
    fetch('components/source/source.html')
        .then(response => response.text())
        .then(data => {
            const source = document.getElementById('source');
            source.innerHTML = data;
        })
        .catch(error => console.error(error));
}

const sourceTab = document.querySelector('#source-tab');

sourceTab.addEventListener('click', () => {
    loadSourceContent();
});
