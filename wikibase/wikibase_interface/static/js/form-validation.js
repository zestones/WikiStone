function validateForm() {
    var query = document.getElementById('input-keyword').value
    var errorMessage = document.getElementById("error-message");

    if (query == "") {
        errorMessage.innerHTML = "Enter something before submitting.";
        errorMessage.style.display = "block";
        return false;
    }

    errorMessage.style.display = "none";
    return true;
}

// Add event listener to "open-search" button
const openSearchBtn = document.querySelector('.open-search');
const container = document.querySelector('.container');
const searchOptions = document.querySelector('.search-options');

// Toogle the container and display search options
openSearchBtn.addEventListener('click', () => {
    searchOptions.classList.toggle('visible');
        container.classList.toggle('expanded');
});
