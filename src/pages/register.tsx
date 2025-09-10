import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

const Register: React.FC = () => {
  const navigate = useNavigate();

  // Form state variables
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");

  // Handle registration
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    //  Debug log: Show form values
    console.log(" Registering user with values:", {
      name,
      email,
      password,
      role,
    });

    try {
      // API call to register user
      const response = await api.post("/users/register", {
        name,
        email,
        password,
        role,
      });

      console.log(" Registration successful:", response.data);
      alert(" Registered successfully. Please login.");
      navigate("/login");
    } catch (err: any) {
      // Show friendly error
      setError(" Registration failed. Try again.");

      //  Detailed error log
      console.error(" Registration error:", err.response || err.message || err);
    }
  };

  return (
    <div className="center" style={{ padding: "2rem" }}>
      <h1>Register</h1>
      <form
        onSubmit={handleRegister}
        style={{ maxWidth: "300px", margin: "0 auto" }}
      >
        <div>
          <label>Name </label>
          <input
            className="input"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: "1rem" }}>
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
          <label>Role </label>
          <select
            className="input"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="student">Student</option>
            <option value="faculty">Faculty</option>
          </select>
        </div>

        <button className="btn" type="submit" style={{ marginTop: "1rem" }}>
          Register
        </button>

        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
      </form>
    </div>
  );
};

export default Register;
