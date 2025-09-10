import { useEffect, useState } from "react";
import api from "../../axios";
import type { User, ActiveUser } from "../../types";

export default function AdminUsers() {
  const [tab, setTab] = useState<"all" | "active">("all");

  const authHeaders = {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };

  const [users, setUsers] = useState<User[]>([]);
  const [activeUsers, setActiveUsers] = useState<ActiveUser[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        if (tab === "all") {
          const res = await api.get("/admin/users", { headers: authHeaders });
          setUsers(res.data);
        } else {
          const res = await api.get("/admin/active-users", {
            headers: authHeaders,
          });
          setActiveUsers(res.data);
        }
      } catch (err) {
        console.error("Failed to fetch users", err);
        setUsers([]);
        setActiveUsers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [tab]);

  return (
    <section>
      <h2>👥 Manage Users</h2>

      {/* Tabs */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          className={`tab-btn ${tab === "all" ? "active" : ""}`}
          onClick={() => setTab("all")}
        >
          All Users
        </button>
        <button
          className={`tab-btn ${tab === "active" ? "active" : ""}`}
          onClick={() => setTab("active")}
        >
          Active Users
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {/* All Users Table */}
      {tab === "all" && !loading && (
        <>
          {users.length === 0 ? (
            <p>No users found.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={tableHeaderStyle}>ID</th>
                  <th style={tableHeaderStyle}>Name</th>
                  <th style={tableHeaderStyle}>Email</th>
                  <th style={tableHeaderStyle}>Role</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id} style={{ borderBottom: "1px solid #ddd" }}>
                    <td style={tableCellStyle}>{user.id}</td>
                    <td style={tableCellStyle}>{user.name}</td>
                    <td style={tableCellStyle}>{user.email}</td>
                    <td style={tableCellStyle}>{user.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      {/* Active Users List */}
      {tab === "active" && !loading && (
        <>
          {activeUsers.length === 0 ? (
            <p>No active users found.</p>
          ) : (
            <div>
              {activeUsers.map((user) => (
                <div
                  key={user.id}
                  style={{
                    background: "#fff",
                    border: "1px solid #ddd",
                    padding: "1rem",
                    borderRadius: "6px",
                    marginBottom: "1rem",
                  }}
                >
                  <h3 style={{ marginBottom: "0.4rem" }}>
                    {user.name} ({user.role})
                  </h3>
                  <p style={{ marginBottom: "0.4rem" }}>
                    Email: {user.email} | Borrowed Books:{" "}
                    {user.borrowed_books.length}
                  </p>

                  {user.borrowed_books.length > 0 && (
                    <table
                      style={{
                        width: "100%",
                        borderCollapse: "collapse",
                        marginTop: "0.5rem",
                      }}
                    >
                      <thead>
                        <tr>
                          <th style={tableHeaderStyle}>Title</th>
                          <th style={tableHeaderStyle}>Borrow Date</th>
                          <th style={tableHeaderStyle}>Due Date</th>
                          <th style={tableHeaderStyle}>Return Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {user.borrowed_books.map((book, i) => (
                          <tr
                            key={i}
                            style={{ borderBottom: "1px solid #ddd" }}
                          >
                            <td style={tableCellStyle}>{book.title}</td>
                            <td style={tableCellStyle}>
                              {new Date(book.borrow_date).toLocaleDateString()}
                            </td>
                            <td style={tableCellStyle}>
                              {new Date(book.due_date).toLocaleDateString()}
                            </td>
                            <td style={tableCellStyle}>
                              {book.return_date
                                ? new Date(
                                    book.return_date
                                  ).toLocaleDateString()
                                : "Not returned"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              ))}
            </div>
          )}
        </>
      )}

      <style>{`
        .tab-btn {
          background: none;
          border: 1px solid #007bff;
          padding: 0.4rem 0.8rem;
          margin-right: 0.5rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.9rem;
        }
        .tab-btn.active,
        .tab-btn:hover {
          background-color: #007bff;
          color: white;
        }
      `}</style>
    </section>
  );
}

const tableHeaderStyle = {
  borderBottom: "2px solid #007bff",
  textAlign: "left" as const,
  padding: "0.5rem",
  backgroundColor: "#e9f0ff",
};

const tableCellStyle = {
  padding: "0.5rem",
};
