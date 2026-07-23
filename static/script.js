let index = 0;
function showSlides() {
  if (document.querySelector(".auth-left .carousel")) {
    return;
  }

  let slides = document.querySelectorAll(".carousel img");
  slides.forEach((slide) => (slide.style.display = "none"));
  index++;
  if (index > slides.length) index = 1;
  slides[index - 1].style.display = "block";
  setTimeout(showSlides, 15000);
}
if (document.querySelector(".carousel")) {
  showSlides();
}

function openLogin() {
  document.getElementById("loginModal").style.display = "flex";
}
function closeLogin() {
  document.getElementById("loginModal").style.display = "none";
}

function loginUser(event) {
  event.preventDefault();
  document.getElementById("loginModal").style.display = "none";
  document.getElementById("loginBtn").style.display = "none";
  document.getElementById("logoutBtn").style.display = "inline";
  alert("Login Successful!");
}
function logoutUser() {
  document.getElementById("loginBtn").style.display = "inline";
  document.getElementById("logoutBtn").style.display = "none";
  alert("Logged Out!");
}

function handleBackendAlerts() {
  if (!Array.isArray(window.backendAlerts) || window.backendAlerts.length === 0) {
    return;
  }

  let redirectAfter = null;
  window.backendAlerts.forEach((message) => {
    if (!message || !message.text) {
      return;
    }

    alert(message.text);

    if (message.text === "Login successful") {
      redirectAfter = "/dashboard/";
    }
    if (message.text === "Already registered") {
      redirectAfter = "/?form=signup";
    }
    if (message.text === "Signup successful. Please login.") {
      redirectAfter = "/?form=login";
    }
  });

  if (redirectAfter && window.location.pathname !== redirectAfter) {
    window.location.href = redirectAfter;
  }
}

function initGentleLoginScroll() {
  const isLoginPage = /\/login(\/|$)/.test(window.location.pathname) || document.querySelector(".auth-container");
  if (!isLoginPage) {
    return;
  }

  const startY = window.scrollY || window.pageYOffset || 0;
  const maxY = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

  if (maxY <= 0 || startY >= maxY) {
    return;
  }

  let startTime = null;
  const duration = 22000;

  function animateScroll(timestamp) {
    if (!startTime) {
      startTime = timestamp;
    }

    const elapsed = timestamp - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 0.5 - Math.cos(progress * Math.PI) / 2;
    const currentY = startY + (maxY - startY) * eased;

    window.scrollTo(0, currentY);

    if (progress < 1) {
      requestAnimationFrame(animateScroll);
    }
  }

  requestAnimationFrame(animateScroll);
}

document.addEventListener("DOMContentLoaded", handleBackendAlerts);
document.addEventListener("DOMContentLoaded", initGentleLoginScroll);
