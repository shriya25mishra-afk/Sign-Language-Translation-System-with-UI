// Check if token exists
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "login.html";
}

// Logout button
const logoutBtn = document.getElementById("logoutBtn");
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "login.html";
});
