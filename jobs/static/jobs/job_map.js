// jobs/static/jobs/job_map.js

let map;
let marker;

document.addEventListener("DOMContentLoaded", function () {
    // Initialize the map centered on the job location
    if (jobData.latitude && jobData.longitude) {
        map = L.map("map").setView([jobData.latitude, jobData.longitude], 12);
    } else {
        // Fallback to USA center if coordinates are missing
        map = L.map("map").setView([37.0902, -95.7129], 4);
    }

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    }).addTo(map);

    // If job has coordinates, add marker and center on it
    if (jobData.latitude && jobData.longitude) {
        marker = L.marker([jobData.latitude, jobData.longitude]).addTo(map);
        marker.bindPopup(
            `<b>${jobData.title}</b><br>
             ${jobData.location}<br>
             ${jobData.salaryRange}<br>
             Skills: ${jobData.skills}<br>
             Remote: ${jobData.remote}<br>
             Visa Sponsorship: ${jobData.visaSponsorship}`
        );
        marker.openPopup();
        map.setView([jobData.latitude, jobData.longitude], 12);
    }
});
