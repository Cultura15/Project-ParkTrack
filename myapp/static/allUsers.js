document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/getUsers/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const usersTableBody = document.querySelector('#users-table tbody');
            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.fname}</td>
                    <td>${user.lname}</td>
                    <td>${user.email}</td>
                    <td>${user.contactNo}</td>
                    <td>${user.address}</td>
                    <td>${user.password}</td>
                    <td>${user.accountType}</td>
                `;
                usersTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});
