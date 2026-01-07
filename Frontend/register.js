const registerForm = document.getElementById("registerForm");

registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!name || !email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5001/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      alert("✅ Registration successful! Please login.");
      window.location.href = "login.html";
    } else {
      alert(data.msg || "❌ Registration failed");
    }
  } catch (err) {
    console.error("Server error:", err);
    alert("❌ Server error. Make sure your backend is running.");
  }
});
