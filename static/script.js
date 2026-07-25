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

function updateToggleUI(theme) {
  const toggleBtns = document.querySelectorAll("#theme-toggle, #theme-btn, .theme-toggle-btn");
  toggleBtns.forEach(btn => {
    const txt = btn.querySelector("#toggle-text") || btn.querySelector(".toggle-text");
    const icon = btn.querySelector("#toggle-icon") || btn.querySelector(".toggle-icon");

    if (theme === "dark") {
      if (txt) txt.textContent = "Light Mode";
      if (icon) icon.textContent = "☀️";
      if (!txt && !icon) btn.textContent = "☀️ Light Mode";
    } else {
      if (txt) txt.textContent = "Dark Mode";
      if (icon) icon.textContent = "🌙";
      if (!txt && !icon) btn.textContent = "🌙 Dark Mode";
    }
  });
}

function initTheme() {
  const savedTheme = localStorage.getItem("theme") || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", savedTheme);
  if (document.body) {
    document.body.setAttribute("data-theme", savedTheme);
  }
  updateToggleUI(savedTheme);
}

let isThemeToggling = false;
function toggleTheme() {
  if (isThemeToggling) return;
  isThemeToggling = true;
  setTimeout(() => { isThemeToggling = false; }, 120);

  const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
  const newTheme = currentTheme === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", newTheme);
  if (document.body) {
    document.body.setAttribute("data-theme", newTheme);
  }
  localStorage.setItem("theme", newTheme);
  updateToggleUI(newTheme);
}

// Make theme functions globally available on window
window.updateToggleUI = updateToggleUI;
window.initTheme = initTheme;
window.toggleTheme = toggleTheme;

function setupThemeToggle() {
  initTheme();
  const toggleBtns = document.querySelectorAll("#theme-toggle, #theme-btn, .theme-toggle-btn");
  toggleBtns.forEach(btn => {
    if (!btn.getAttribute("onclick")) {
      btn.removeEventListener("click", toggleTheme);
      btn.addEventListener("click", toggleTheme);
    }
  });
}

// Initialize theme immediately on script execute
initTheme();

// Auto-synchronize theme across all open tabs & pages when toggle button is clicked
window.addEventListener("storage", function (e) {
  if (e.key === "theme" && e.newValue) {
    document.documentElement.setAttribute("data-theme", e.newValue);
    if (document.body) {
      document.body.setAttribute("data-theme", e.newValue);
    }
    updateToggleUI(e.newValue);
  }
});

function initDashboardParallax() {
  const scrollContainer = document.querySelector(".page-content-scroll");
  const heroElement = document.getElementById("dashboardHero");
  const bgLayer = document.getElementById("parallaxBg");
  const contentLayer = document.getElementById("parallaxContent");
  const cardLayer = document.getElementById("parallaxCard");

  if (!heroElement) return;

  function onScroll() {
    const scrollTop = scrollContainer ? scrollContainer.scrollTop : window.scrollY || 0;
    if (scrollTop < 900) {
      if (bgLayer) bgLayer.style.transform = `translate3d(0, ${scrollTop * 0.3}px, 0) scale(1.05)`;
      if (contentLayer) contentLayer.style.transform = `translate3d(0, ${scrollTop * 0.15}px, 0)`;
      if (cardLayer) cardLayer.style.transform = `translate3d(0, ${scrollTop * -0.18}px, 0)`;
    }
  }

  const target = scrollContainer || window;
  target.removeEventListener("scroll", onScroll);
  target.addEventListener("scroll", onScroll, { passive: true });
}

document.addEventListener("DOMContentLoaded", handleBackendAlerts);
document.addEventListener("DOMContentLoaded", initGentleLoginScroll);
document.addEventListener("DOMContentLoaded", setupThemeToggle);
document.addEventListener("DOMContentLoaded", initDashboardParallax);




