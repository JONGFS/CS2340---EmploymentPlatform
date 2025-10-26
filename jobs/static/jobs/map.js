// jobs/static/jobs/map.js

let map;
let markers = [];
let currentLocationMarker;

document.addEventListener("DOMContentLoaded", function () {
    // Initialize the map
    map = L.map("map").setView([37.0902, -95.7129], 4); // USA center

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(map);

    // Add location filter controls
    const filterControl = L.control({ position: 'topright' });
    filterControl.onAdd = function () {
        const div = L.DomUtil.create('div', 'location-filter leaflet-bar');
        div.innerHTML = `
            <div class="p-2 bg-white" style="min-width: 220px;">
                <input type="text" id="locationInput" class="form-control mb-2" placeholder="Enter your location">
                <select id="distanceFilter" class="form-control mb-2">
                    <option value="">Select distance</option>
                    <option value="25">Within 25 miles</option>
                    <option value="50">Within 50 miles</option>
                </select>
                <button onclick="filterByLocation()" class="btn btn-primary btn-sm w-100">Filter Jobs</button>
                <button onclick="resetFilter()" class="btn btn-secondary btn-sm w-100 mt-2">Reset Filter</button>
            </div>
        `;
        return div;
    };
    filterControl.addTo(map);

    // Load initial jobs
    loadJobs();

    // Optional: get user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const { latitude, longitude } = pos.coords;
                document.getElementById('locationInput').value = 'Current Location';
                filterByLocation(latitude, longitude);
            },
            (err) => console.warn("Geolocation not allowed:", err)
        );
    }
});

function loadJobs() {
    fetch("/jobs/api/")
        .then((response) => response.json())
        .then((data) => {
            // Clear existing markers
            markers.forEach(marker => marker.remove());
            markers = [];

            // Add new markers
            data.jobs.forEach((job) => {
                if (job.latitude && job.longitude) {
                    const marker = L.marker([job.latitude, job.longitude]);
                    marker.bindPopup(
                        `<b>${job.title}</b><br>
                         ${job.location}<br>
                         ${job.salaryRange}<br>
                         Skills: ${job.skills}<br>
                         Remote: ${job.remote}<br>
                         Visa Sponsorship: ${job.visaSponsorship}`
                    );
                    marker.jobData = job; // Store job data with marker
                    markers.push(marker);
                    marker.addTo(map);
                }
            });
        })
        .catch((error) => {
            console.error("Error loading job data:", error);
        });
}

function filterByLocation(predefinedLat, predefinedLng) {
    const locationInput = document.getElementById('locationInput').value;
    const distance = document.getElementById('distanceFilter').value;
    
    if (!locationInput || !distance) {
        alert('Please enter both location and distance');
        return;
    }

    if (predefinedLat && predefinedLng) {
        // Use predefined coordinates (e.g., from geolocation)
        applyFilter(predefinedLat, predefinedLng, distance);
    } else {
        // Use OpenStreetMap Nominatim API to get coordinates from location input
        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationInput)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    alert('Location not found. Please try a different location.');
                    return;
                }
                applyFilter(parseFloat(data[0].lat), parseFloat(data[0].lon), distance);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error finding location. Please try again.');
            });
    }
}

function applyFilter(lat, lng, distance) {
    // Update user location marker
    if (currentLocationMarker) {
        currentLocationMarker.remove();
    }
    currentLocationMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'current-location-marker',
            html: '📍',
            iconSize: [25, 25],
            iconAnchor: [12, 24]
        })
    }).addTo(map);

    // Filter and show only jobs within the selected distance
    markers.forEach(marker => {
        const jobLat = marker.jobData.latitude;
        const jobLng = marker.jobData.longitude;
        const distanceToJob = calculateDistance(lat, lng, jobLat, jobLng);
        
        if (distanceToJob <= distance) {
            marker.addTo(map);
        } else {
            marker.remove();
        }
    });

    // Center map on user location with appropriate zoom
    map.setView([lat, lng], 10);
}

function resetFilter() {
    // Remove current location marker
    if (currentLocationMarker) {
        currentLocationMarker.remove();
    }

    // Reset form inputs
    document.getElementById('locationInput').value = '';
    document.getElementById('distanceFilter').value = '';

    // Show all markers again
    markers.forEach(marker => marker.addTo(map));

    // Reset map view to USA
    map.setView([37.0902, -95.7129], 4);
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    // Haversine formula to calculate distance between two points
    const R = 3958.8; // Earth's radius in miles
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c; // Distance in miles
}

function toRad(degrees) {
    return degrees * (Math.PI / 180);
}
