function validateForm() {
    var query = document.getElementById('input-field').value
    var errorMessage = document.getElementById("error-message");

    if (query == "") {
        errorMessage.innerHTML = "Enter something before submitting.";
        errorMessage.style.display = "block";
        return false;
    }

    errorMessage.style.display = "none";
    return true;
}