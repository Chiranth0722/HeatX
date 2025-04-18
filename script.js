// Load header and footer from components
document.addEventListener("DOMContentLoaded", () => {
    fetch("components/header.html")
      .then((res) => res.text())
      .then((data) => document.getElementById("main-header").innerHTML = data);
  
    fetch("components/footer.html")
      .then((res) => res.text())
      .then((data) => document.getElementById("main-footer").innerHTML = data);
  });
  