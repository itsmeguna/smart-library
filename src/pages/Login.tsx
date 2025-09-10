import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios"; // Axios instance for API calls

const Login: React.FC = () => {
  const navigate = useNavigate();

  //  Form state values
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user"); // default role
  const [error, setError] = useState("");

  //  Handle form submission
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // 🔍 Debug log: Attempt login
    console.log("Attempting login with:", { email, role });

    try {
      // Choose login endpoint based on role
      const endpoint = role === "admin" ? "/admin/login" : "/users/login";

      const response = await api.post(endpoint, {
        email,
        password,
      });

      const { access_token } = response.data;

      // Log received token
      console.log(" Login successful. Token received:", access_token);

      // Store token and role in localStorage
      localStorage.setItem("token", access_token);
      localStorage.setItem("role", role);

      // Navigate to search page after login
      if (role === "user") {
        navigate("/user");
      } else if (role === "admin") {
        navigate("/admin");
      }
    } catch (err: any) {
      console.error(" Login error:", err);
      setError("Login failed. Please check credentials.");
    }
  };

  return (
    <div className="center" style={{ padding: "2rem" }}>
      <h1>Login</h1>

      <form
        onSubmit={handleLogin}
        style={{ maxWidth: "300px", margin: "0 auto" }}
      >
        <div>
          <label>Email </label>
          <input
            className="input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: "1rem" }}>
          <label>Password </label>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: "1rem" }}>
          <label>Login as </label>
          <select
            className="input"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="user">User (Student/Faculty)</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button className="btn" type="submit" style={{ marginTop: "1rem" }}>
          Login
        </button>

        <p style={{ marginTop: "1rem" }}>
          Don't have an account?{" "}
          <a
            href="/register"
            style={{ color: "#007bff", textDecoration: "underline" }}
          >
            Register here
          </a>
        </p>

        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
      </form>
    </div>
  );
};

export default Login;
