// jobs/static/jobs/map.js

let map;
let markers = [];
let currentLocationMarker;
let radiusCircle;
const AVERAGE_SPEED_MPH = 35; // used to estimate driving minutes from straight-line miles

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
    <div class="p-2 bg-white" style="min-width: 240px;">
      <input type="text" id="locationInput" class="form-control mb-2" placeholder="Enter your location">

      <select id="distanceFilter" class="form-control mb-2">
        <option value="">Select distance</option>
        <option value="10">Within 10 miles</option>
        <option value="25">Within 25 miles</option>
        <option value="50">Within 50 miles</option>
      </select>
      
      <button onclick="filterByLocation()" class="btn btn-primary btn-sm w-100">Filter Jobs</button>
      <button onclick="resetFilter()" class="btn btn-secondary btn-sm w-100 mt-2">Reset Filter</button>
    </div>`;
    L.DomEvent.disableClickPropagation(div);
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
                    // Initial popup without distance (will be updated when a location filter is applied)
                    marker.bindPopup(
                        `<b>${job.title}</b><br>
                         ${job.location}<br>
                         ${job.salaryRange}<br>
                         Skills: ${job.skills}<br>
                         Remote: ${job.remote}<br>
                         Visa Sponsorship: ${job.visaSponsorship}<br>
                         <small class="job-distance">Distance: N/A</small>`
                    );
                    marker.jobData = job; // Store job data with marker
                    markers.push(marker);
                    // When marker is clicked, if we have a current location, update popup with distance/time
                    marker.on('click', function () {
                        if (currentLocationMarker) {
                            const userLat = currentLocationMarker.getLatLng().lat;
                            const userLng = currentLocationMarker.getLatLng().lng;
                            const d = calculateDistance(userLat, userLng, marker.jobData.latitude, marker.jobData.longitude);
                            const distanceStr = `${d.toFixed(1)} miles`;
                            const estimatedMinutes = Math.max(1, Math.round((d / AVERAGE_SPEED_MPH) * 60));
                            const timeStr = `${estimatedMinutes} min`;
                            const popupHtml = `
                                <b>${marker.jobData.title}</b><br>
                                ${marker.jobData.location}<br>
                                ${marker.jobData.salaryRange}<br>
                                Skills: ${marker.jobData.skills}<br>
                                Remote: ${marker.jobData.remote}<br>
                                Visa Sponsorship: ${marker.jobData.visaSponsorship}<br>
                                <small class="job-distance">Distance: ${distanceStr} (~${timeStr} drive)</small>
                            `;
                            if (marker.getPopup && marker.getPopup()) {
                                try { marker.getPopup().setContent(popupHtml); }
                                catch (e) { marker.bindPopup(popupHtml); }
                            } else { marker.bindPopup(popupHtml); }
                        }
                    });
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
        alert('Please enter a location and select a distance');
        return;
    }
    
    const applyFilterHelper = (lat, lng) => applyFilter(lat, lng, distance);

    if (predefinedLat && predefinedLng) {
        // Use predefined coordinates (e.g., from geolocation)
        applyFilterHelper(predefinedLat, predefinedLng);
    } else {
        // Use OpenStreetMap Nominatim API to get coordinates from location input
        console.log('Fetching location for:', locationInput);
        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationInput)}`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Geocoding data:', data);
                if (data.length === 0) {
                    alert(`Location "${locationInput}" not found. Please try a different location.`);
                    return;
                }
                const coords = { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
                console.log('Coordinates found:', coords);
                applyFilterHelper(coords.lat, coords.lon);
            })
            .catch(error => {
                console.error('Geocoding error:', error);
                alert(`Error finding location "${locationInput}": ${error.message}. Please try again.`);
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
    if (radiusCircle) { 
        radiusCircle.remove();
    }
    radiusCircle = L.circle([lat, lng], { 
        radius: distance * 1609.344, // Convert miles to meters
        color: '#3388ff',
        fillColor: '#3388ff',
        fillOpacity: 0.1,
        weight: 2
    }).addTo(map);
  
    markers.forEach(marker => {
        const d = calculateDistance(lat, lng, marker.jobData.latitude, marker.jobData.longitude);
        // Build a more informative popup including distance (miles) and estimated drive time (minutes)
        const distanceStr = `${d.toFixed(1)} miles`;
        const estimatedMinutes = Math.max(1, Math.round((d / AVERAGE_SPEED_MPH) * 60));
        const timeStr = `${estimatedMinutes} min`;
        const popupHtml = `
            <b>${marker.jobData.title}</b><br>
            ${marker.jobData.location}<br>
            ${marker.jobData.salaryRange}<br>
            Skills: ${marker.jobData.skills}<br>
            Remote: ${marker.jobData.remote}<br>
            Visa Sponsorship: ${marker.jobData.visaSponsorship}<br>
            <small class="job-distance">Distance: ${distanceStr} (~${timeStr} drive)</small>
        `;

        // Update popup content if a popup already exists, otherwise bind a new popup
        if (marker.getPopup && marker.getPopup()) {
            try {
                marker.getPopup().setContent(popupHtml);
            } catch (e) {
                marker.bindPopup(popupHtml);
            }
        } else {
            marker.bindPopup(popupHtml);
        }

        if (d <= distance) {
            marker.addTo(map);
        } else {
            marker.remove();
        }
    });
  
    map.setView([lat, lng], Math.max(8, Math.min(12, Math.floor(12 - Math.log2(distance/10)))));
}

function resetFilter() {
    // Remove current location marker
    if (currentLocationMarker) {
        currentLocationMarker.remove();
    }
    
    // Remove radius circle
    if (radiusCircle) {
        radiusCircle.remove();
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


