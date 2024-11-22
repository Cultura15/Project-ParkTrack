document.getElementById('login-form').onsubmit = async function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const formData = new FormData(this);
    const data = Object.fromEntries(formData); // Convert form data to a plain object

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data) // Convert the object to JSON
        });

        const result = await response.json();
        console.log('API Response:', result); // Log the response to the console

        // Handle response
        if (response.ok) {
            // Check if userId exists in the result
            if (result.user && result.user.userId) {
                const userId = result.user.userId;
                console.log('userId:', userId);  // Check userId in the console
                localStorage.setItem('userId', userId);  // Save the userId to localStorage

                alert('Login successful!');
                window.location.href = '/menu/';
            } else {
                alert('userId is missing in the response');
            }
        } else {
            alert(`Error: ${result.error || 'Login failed'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login.');
    }
};
