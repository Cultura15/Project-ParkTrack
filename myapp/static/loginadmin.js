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
            // Ensure the user object exists and has userId and email
            if (result.user && result.user.userId && result.user.email) {
                const userId = result.user.userId;
                console.log('userId:', userId);  // Check userId in the console
                localStorage.setItem('userId', userId);  // Save the userId to localStorage

                // Check if the logged-in user is the admin
                if (result.user.email === 'admin@gmail.com') {
                    console.log('Admin user detected, redirecting...');
                    window.location.href = 'http://127.0.0.1:8000/api/admin1/'; // Redirect to the admin page
                } else {
                    alert('Login successful!');
                    window.location.href = '/menu/'; // Redirect to menu if not admin
                }
            } else {
                window.location.href = 'http://127.0.0.1:8000/api/admin1/'; 
                alert('Logged in as admin');
                console.log('Result:', result);  // Log the entire result to inspect its structure
            }
        } else {
            alert(`Error: ${result.error || 'Login failed'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login.');
    }
};
