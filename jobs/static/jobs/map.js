// jobs/static/jobs/map.js

document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("map").setView([37.0902, -95.7129], 4); // USA center

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Fetch job data from the backend
  fetch("/jobs/api/")
    .then((response) => response.json())
    .then((data) => {
      data.jobs.forEach((job) => {
        if (job.latitude && job.longitude) {
          const marker = L.marker([job.latitude, job.longitude]).addTo(map);
          marker.bindPopup(
            `<b>${job.title}</b><br>${job.location}<br>${job.salaryRange}<br>${job.remote}`
          );
        }
      });
    })
    .catch((error) => {
      console.error("Error loading job data:", error);
    });

  // Optional: get user location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        map.setView([latitude, longitude], 10);
        L.circle([latitude, longitude], {
          radius: 1000,
          color: "blue",
          fillOpacity: 0.3,
        }).addTo(map).bindPopup("You are here");
      },
      (err) => console.warn("Geolocation not allowed:", err)
    );
  }
});
