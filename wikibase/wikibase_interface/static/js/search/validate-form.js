export function validateForm(formData) {

    // Check if no search criteria have been provided
    if (!formData.query && !formData.city && !formData.postalCode && !formData.region) {

        // Display error message
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerHTML = 'Please provide at least one search criteria.';
        errorMessage.style.display = 'block';

        // Return false to indicate that the form is not valid
        return false;
    }

    // Hide error message
    const errorMessage = document.getElementById('error-message');
    errorMessage.style.display = 'none';

    // Return true to indicate that the form is valid
    return true;
}