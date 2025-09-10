import { useEffect, useState } from "react";
import api from "../../axios";
import type {
  MostBorrowedBook,
  MonthlyUsageItem,
  OverdueBookItem,
} from "../../types";

export default function AdminReports() {
  const [reportTab, setReportTab] = useState<
    "mostBorrowed" | "monthlyUsage" | "overdueBooks"
  >("mostBorrowed");

  const authHeaders = {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };

  const [mostBorrowed, setMostBorrowed] = useState<MostBorrowedBook[]>([]);
  const [monthlyUsage, setMonthlyUsage] = useState<MonthlyUsageItem[]>([]);
  const [overdueBooks, setOverdueBooks] = useState<OverdueBookItem[]>([]);

  // Fetch report data
  useEffect(() => {
    const fetchMostBorrowed = async () => {
      const res = await api.get("/admin/most_borrowed", {
        headers: authHeaders,
      });
      setMostBorrowed(
        res.data.map((item: any) => ({
          title: item.title,
          author: item.author,
          isbn: item.isbn,
          borrow_count: item.borrow_count,
        }))
      );
    };

    const fetchMonthlyUsage = async () => {
      const res = await api.get("/admin/monthly_usage", {
        headers: authHeaders,
      });
      setMonthlyUsage(res.data);
    };

    const fetchOverdueBooks = async () => {
      const res = await api.get("/admin/overdue-books", {
        headers: authHeaders,
      });
      const now = new Date();
      setOverdueBooks(
        res.data.map((item: any) => ({
          user_name: item.user_name,
          email: item.email,
          title: item.book_title,
          due_date: item.due_date,
          days_overdue: Math.max(
            0,
            Math.floor(
              (now.getTime() - new Date(item.due_date).getTime()) /
                (1000 * 60 * 60 * 24)
            )
          ),
        }))
      );
    };

    if (reportTab === "mostBorrowed") fetchMostBorrowed();
    if (reportTab === "monthlyUsage") fetchMonthlyUsage();
    if (reportTab === "overdueBooks") fetchOverdueBooks();
  }, [reportTab, authHeaders]);

  return (
    <section>
      <h2>📊 Reports</h2>
      <div style={{ marginBottom: "1rem" }}>
        <button
          className={`report-btn ${
            reportTab === "mostBorrowed" ? "active" : ""
          }`}
          onClick={() => setReportTab("mostBorrowed")}
        >
          Most Borrowed Books
        </button>
        <button
          className={`report-btn ${
            reportTab === "monthlyUsage" ? "active" : ""
          }`}
          onClick={() => setReportTab("monthlyUsage")}
        >
          Monthly Usage
        </button>
        <button
          className={`report-btn ${
            reportTab === "overdueBooks" ? "active" : ""
          }`}
          onClick={() => setReportTab("overdueBooks")}
        >
          Overdue Books
        </button>
      </div>

      {/* Most Borrowed Books */}
      {reportTab === "mostBorrowed" && (
        <>
          {mostBorrowed.length === 0 ? (
            <p>No data found.</p>
          ) : (
            <table className="report-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Author</th>
                  <th>ISBN</th>
                  <th>Borrow Count</th>
                </tr>
              </thead>
              <tbody>
                {mostBorrowed.map((b, idx) => (
                  <tr key={idx}>
                    <td>{b.title}</td>
                    <td>{b.author}</td>
                    <td>{b.isbn}</td>
                    <td>{b.borrow_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      {/* Monthly Usage */}
      {reportTab === "monthlyUsage" && (
        <>
          {monthlyUsage.length === 0 ? (
            <p>No monthly usage found.</p>
          ) : (
            <table className="report-table">
              <thead>
                <tr>
                  <th>Book Title</th>
                  <th>User Name</th>
                  <th>Borrow Date</th>
                  <th>Return Date</th>
                  <th>Overdue</th>
                </tr>
              </thead>
              <tbody>
                {monthlyUsage.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.book_title}</td>
                    <td>{item.user_name}</td>
                    <td>{new Date(item.borrow_date).toLocaleString()}</td>
                    <td>
                      {item.return_date
                        ? new Date(item.return_date).toLocaleString()
                        : "Not Returned"}
                    </td>
                    <td>{item.overdue ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      {/* Overdue Books */}
      {reportTab === "overdueBooks" && (
        <>
          {overdueBooks.length === 0 ? (
            <p>No overdue books found.</p>
          ) : (
            <table className="report-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Book Title</th>
                  <th>Due Date</th>
                  <th>Days Overdue</th>
                </tr>
              </thead>
              <tbody>
                {overdueBooks.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.user_name}</td>
                    <td>{item.email}</td>
                    <td>{item.title}</td>
                    <td>{new Date(item.due_date).toLocaleDateString()}</td>
                    <td>{item.days_overdue}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      <style>{`
        .report-btn {
          background: none;
          border: 1px solid #007bff;
          padding: 0.3rem 0.7rem;
          margin-right: 0.5rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.9rem;
        }
        .report-btn.active,
        .report-btn:hover {
          background-color: #007bff;
          color: white;
        }
        .report-table {
          width: 100%;
          border-collapse: collapse;
        }
        .report-table th, .report-table td {
          padding: 0.5rem;
          border-bottom: 1px solid #ddd;
        }
      `}</style>
    </section>
  );
}
