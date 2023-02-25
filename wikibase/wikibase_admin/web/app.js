// Expose functions to Python
eel.expose(say_hello_js);
function say_hello_js(x) {
    console.log("Hello from " + x);
}


const links = document.querySelectorAll('.sidebar li a');

links.forEach(link => {
    link.addEventListener('click', () => {
        links.forEach(otherLink => otherLink.parentElement.classList.remove('active'));
        link.parentElement.classList.add('active');
    });
});


const pageTitles = {
    'Home': 'Home',
    'Source': 'Document',
    'Property': 'Property',
    'Settings': 'Settings'
};

const sidebar = document.querySelector('.sidebar');
const pageTitlesElement = document.querySelector('.page-title');

sidebar.addEventListener('click', (event) => {
    event.preventDefault();

    const activeElement = document.querySelector('.sidebar li.active');
    const title = activeElement.dataset.title;

    // Update the page title
    pageTitlesElement.textContent = pageTitles[title];
});
