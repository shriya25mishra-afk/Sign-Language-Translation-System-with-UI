const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5001/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Save JWT token in localStorage for later authenticated requests
      localStorage.setItem("token", data.token);
      localStorage.setItem("name", data.name);
      localStorage.setItem("email", data.email);

      alert(`✅ Login successful! Welcome, ${data.name}`);
      // Redirect to profile page or dashboard
      window.location.href = "dashboard.html";
    } else {
      alert(data.error || "❌ Login failed");
    }
  } catch (err) {
    console.error("Server error:", err);
    alert("❌ Server error. Make sure your backend is running.");
  }
});
