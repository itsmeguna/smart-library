import React from "react";
import { useNavigate } from "react-router-dom";

// Reusable Logout Button Component
const LogoutButton: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    console.log(" Logging out...");
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login"); // Redirect to login
  };

  return (
    <button
      onClick={handleLogout}
      className="btn"
      style={{ marginBottom: "1rem" }}
    >
      Logout
    </button>
  );
};

export default LogoutButton;
