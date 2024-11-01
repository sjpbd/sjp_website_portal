let map;
let markers = [];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 39.8283, lng: -98.5795 },
        zoom: 4,
        styles: [
            {
                featureType: "all",
                elementType: "labels.text.fill",
                stylers: [{ color: "#7c93a3" }, { lightness: "-10" }]
            },
            {
                featureType: "administrative.country",
                elementType: "geometry",
                stylers: [{ visibility: "on" }]
            },
            {
                featureType: "administrative.country",
                elementType: "geometry.stroke",
                stylers: [{ color: "#a0a4a5" }]
            },
            {
                featureType: "administrative.province",
                elementType: "geometry.stroke",
                stylers: [{ color: "#62838e" }]
            },
            {
                featureType: "landscape",
                elementType: "geometry.fill",
                stylers: [{ color: "#dde3e3" }]
            },
            {
                featureType: "landscape.man_made",
                elementType: "geometry.stroke",
                stylers: [{ color: "#3f4a51" }, { weight: "0.30" }]
            },
            {
                featureType: "poi",
                elementType: "all",
                stylers: [{ visibility: "simplified" }]
            },
            {
                featureType: "road.highway",
                elementType: "geometry.fill",
                stylers: [{ color: "#ffeba1" }]
            },
            {
                featureType: "road.highway",
                elementType: "geometry.stroke",
                stylers: [{ weight: "0.30" }]
            },
            {
                featureType: "water",
                elementType: "geometry.fill",
                stylers: [{ color: "#a6cbe3" }]
            }
        ]
    });

    displayResults(ministries);
}

function displayResults(results) {
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';
    markers.forEach(marker => marker.setMap(null));
    markers = [];

    results.forEach(ministry => {
        const card = document.createElement('div');
        card.className = 'ministry-card';
        card.innerHTML = `
            <h2>${ministry.name}</h2>
            <p><i class="fas fa-tag"></i> ${ministry.type}</p>
            <p><i class="fas fa-map-marker-alt"></i> ${ministry.location}</p>
            <button onclick="showDetails(${ministry.id})">Learn More</button>
        `;
        resultsContainer.appendChild(card);

        const marker = new google.maps.Marker({
            position: { lat: ministry.lat, lng: ministry.lng },
            map: map,
            title: ministry.name,
            animation: google.maps.Animation.DROP
        });
        markers.push(marker);

        marker.addListener('click', () => {
            showDetails(ministry.id);
        });
    });

    if (results.length > 0) {
        map.setCenter({ lat: results[0].lat, lng: results[0].lng });
        map.setZoom(5);
    }
}

function showDetails(id) {
    const ministry = ministries.find(m => m.id === id);
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h2>${ministry.name}</h2>
        <p><strong>Type:</strong> ${ministry.type}</p>
        <p><strong>Location:</strong> ${ministry.location}</p>
        <p><strong>Description:</strong> ${ministry.description}</p>
        <p><strong>Contact:</strong> ${ministry.contact}</p>
        <p><strong>Website:</strong> <a href="${ministry.website}" target="_blank">${ministry.website}</a></p>
    `;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

function searchAndFilter() {
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const filterSelect = document.getElementById('filter-select');

    const searchTerm = searchInput.value.toLowerCase();
    const sortBy = sortSelect.value;
    const filterBy = filterSelect.value;

    let results = ministries.filter(ministry => 
        (ministry.name.toLowerCase().includes(searchTerm) ||
        ministry.type.toLowerCase().includes(searchTerm) ||
        ministry.location.toLowerCase().includes(searchTerm)) &&
        (filterBy === 'all' || ministry.type === filterBy)
    );

    results.sort((a, b) => {
        if (sortBy === 'name') {
            return a.name.localeCompare(b.name);
        } else if (sortBy === 'location') {
            return a.location.localeCompare(b.location);
        } else {
            return a.type.localeCompare(b.type);
        }
    });

    displayResults(results);
}

document.getElementById('search-btn').addEventListener('click', searchAndFilter);
document.getElementById('search-input').addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        searchAndFilter();
    }
});
document.getElementById('sort-select').addEventListener('change', searchAndFilter);
document.getElementById('filter-select').addEventListener('change', searchAndFilter);

window.onload = () => {
    initMap();
    displayResults(ministries);
};
