function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required]');
    
    for (let input of inputs) {
        if (!input.value) {
            alert('Please fill in all required fields.');
            return false;
        }
    }
    
    return true;
}