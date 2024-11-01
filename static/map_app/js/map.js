document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map
    var map = L.map('map').setView([23.6850, 90.3563], 7);  // Center of Bangladesh

    // Add the tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var missionInfo = document.getElementById('mission-info');

    // Fetch mission data
    fetch('/api/missions/')
        .then(response => response.json())
        .then(missions => {
            console.log('Missions data:', missions);  // Debug: Log the missions data
            missions.forEach(mission => {
                console.log('Creating marker for:', mission.name);  // Debug: Log each mission
                var marker = L.marker([mission.latitude, mission.longitude]).addTo(map);
                marker.on('click', function() {
                    var content = `
                        <h3>${mission.name}</h3>
                        <p><strong>Type:</strong> ${mission.mission_type__name}</p>
                        <p><strong>Address:</strong> ${mission.address}</p>
                        <p><strong>Established:</strong> ${mission.established_date}</p>
                    `;
                    missionInfo.innerHTML = content;
                });
            });
        })
        .catch(error => console.error('Error fetching missions:', error));
});