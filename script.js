// Load header and footer from components
document.addEventListener("DOMContentLoaded", () => {
  fetch("components/header.html")
    .then((res) => res.text())
    .then((data) => {
      document.getElementById("main-header").innerHTML = data;
      setupDropdownToggle(); // call after header loads
    });

  fetch("components/footer.html")
    .then((res) => res.text())
    .then((data) => {
      document.getElementById("main-footer").innerHTML = data;
    });
});

// Setup dropdown toggle after header loads
function setupDropdownToggle() {
  const profileWrapper = document.querySelector(".profile-wrapper");

  if (!profileWrapper) return;

  document.addEventListener("click", function (event) {
    const isClickInside = profileWrapper.contains(event.target);
    
    if (isClickInside) {
      // Toggle dropdown
      profileWrapper.classList.toggle("show-dropdown");
    } else {
      // Close if clicked outside
      profileWrapper.classList.remove("show-dropdown");
    }
  });
}
function setupLogout() {
  const logoutBtn = document.getElementById("logout-btn");
  if (!logoutBtn) return;

  logoutBtn.addEventListener("click", function (e) {
    e.preventDefault();

    // Simulate logout
    localStorage.clear(); // Clear stored user data
    sessionStorage.clear(); // Clear session data if any

    alert("Logged out successfully!");

    // Redirect to login page
    window.location.href = "../login.html"; // Change path as per your project
  });
}
