function validateForm() {
    var query = document.getElementById('input-field').value
    var errorMessage = document.getElementById("error-message");

    if (query == "") {
        errorMessage.innerHTML = "Please enter a monument before sumitting.";
        errorMessage.style.display = "block";
        return false;
    }

    errorMessage.style.display = "none";
    return true;
}