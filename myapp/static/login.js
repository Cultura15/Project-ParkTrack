document.getElementById('login-form').onsubmit = async function (event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const formData = new FormData(this);
    const data = Object.fromEntries(formData); // Convert form data to a plain object

    // Function to create and show the loading screen dynamically
    function showLoadingScreen() {
        const staticUrl = document.body.getAttribute('data-static-url'); // Retrieve the base static URL
        const loadingScreen = document.createElement('div');
        loadingScreen.id = 'loading-screen';
        loadingScreen.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        `;
        const loadingImage = document.createElement('img');
        loadingImage.src = "/static/loading1.gif";  // Dynamically set the path to the static GIF
        loadingImage.alt = "Loading...";
        loadingImage.style.cssText = "width: 100px; height: 100px;";
        loadingScreen.appendChild(loadingImage);
        document.body.appendChild(loadingScreen);
    }
    

    // Function to hide the loading screen
    function hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.remove();
        }
    }

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
            if (result.user && result.user.userId) {
                const userId = result.user.userId;
                console.log('userId:', userId); // Check userId in the console
                localStorage.setItem('userId', userId); // Save the userId to localStorage

                // Show loading screen
                showLoadingScreen();

                // Redirect after 2 seconds
                setTimeout(() => {
                    window.location.href = '/menu/';
                }, 2000);
            } else {
                alert('userId is missing in the response');
            }
        } else {
            alert(`Error: ${result.error || 'Login failed'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login.');
    } finally {
        // Always hide the loading screen unless user successfully logged in
        if (!response.ok || !(result.user && result.user.userId)) {
            hideLoadingScreen();
        }
    }
};


