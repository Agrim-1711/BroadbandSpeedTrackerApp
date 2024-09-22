document.addEventListener('DOMContentLoaded', function () {
    const startTestButton = document.getElementById('startTest');
    const speedTable = document.getElementById('speedTable');

    // Run speed test when button is clicked
    startTestButton.addEventListener('click', async function () {
        try {
            const response = await fetch('http://127.0.0.1:8000/speedtest', {
                method: 'POST'
            });
            const result = await response.json();
            console.log(result);
            alert('Speed test completed!');

            // Refresh speed table data after test
            fetchSpeedData();
        } catch (error) {
            console.error('Error running speed test:', error);
        }
    });

    // Fetch and display speed data from the backend
    async function fetchSpeedData() {
        try {
            const response = await fetch('http://127.0.0.1:8000/speedtest/results', {
                method: 'GET'
            });
            const data = await response.json();

            // Clear existing table rows
            speedTable.innerHTML = '';

            // Populate the table with new data
            data.forEach(speed => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date(speed.date).toLocaleDateString()}</td>
                    <td>${speed.time}</td>
                    <td>${speed.download_speed}</td>
                    <td>${speed.upload_speed}</td>
                    <td>${speed.ping}</td>
                `;
                speedTable.appendChild(row);
            });
        } catch (error) {
            console.error('Error fetching speed data:', error);
        }
    }

    // Initial fetch of speed data on page load
    fetchSpeedData();
});
