document.getElementById('registration-form').onsubmit = async function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const formData = new FormData(this);
    const data = Object.fromEntries(formData); // Convert form data to a plain object

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // Convert the object to JSON
        });

        const result = await response.json();
        console.log(result);

        // Handle response
        if (response.ok) {
            alert('Registration successful!');
            window.location.href = '/api/login/'; // Redirect to login page after successful registration
        } else {
            alert(`Error: ${result.error || 'Registration failed'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration.');
    }
};
