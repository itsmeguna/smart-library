import { useState } from "react";
import AdminBooks from "./AdminBooks";
import AdminUsers from "./AdminUsers ";
import AdminReports from "./AdminReports ";

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<"books" | "users" | "reports">(
    "books"
  );

  //const authHeaders = {
  //  Authorization: `Bearer ${localStorage.getItem("token")}`,
  //};

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* Sidebar */}
      <nav
        style={{
          width: 220,
          borderRight: "1px solid #ccc",
          padding: "1rem",
          background: "#f9f9f9",
        }}
      >
        <h2 style={{ marginBottom: "1rem" }}>Admin Dashboard</h2>
        <button
          className={`nav-btn ${activeTab === "books" ? "active" : ""}`}
          onClick={() => setActiveTab("books")}
        >
          📚 Books
        </button>
        <button
          className={`nav-btn ${activeTab === "users" ? "active" : ""}`}
          onClick={() => setActiveTab("users")}
        >
          👥 Active Users
        </button>
        <button
          className={`nav-btn ${activeTab === "reports" ? "active" : ""}`}
          onClick={() => setActiveTab("reports")}
        >
          📊 Reports
        </button>
        <style>{`
          .nav-btn {
            width: 100%;
            text-align: left;
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 1rem;
            border-radius: 4px;
          }
          .nav-btn.active, .nav-btn:hover {
            background-color: #007bff;
            color: white;
          }
        `}</style>
      </nav>

      {/* Main content */}
      <main style={{ flex: 1, padding: "1.5rem", overflowY: "auto" }}>
        {activeTab === "books" && <AdminBooks />}
        {activeTab === "users" && <AdminUsers />}
        {activeTab === "reports" && <AdminReports />}
      </main>
    </div>
  );
}
