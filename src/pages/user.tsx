// src/pages/UserDashboard.tsx
import React, { useEffect, useState } from "react";
import type { Book, BorrowedBook, OverdueBook } from "../types";
import api from "../axios";
import LogoutButton from "../components/logout";
//import { getMyBooks } from "../services/user";

const UserDashboard: React.FC = () => {
  // Search term for finding books
  const [search, setSearch] = useState("");
  // Search results
  const [books, setBooks] = useState<Book[]>([]);

  // Borrowed books list
  const [borrowedBooks, setBorrowedBooks] = useState<BorrowedBook[]>([]);
  // Overdue books list
  const [overdueBooks, setOverdueBooks] = useState<OverdueBook[]>([]);

  const [error, setError] = useState("");

  // Fetch borrowed & overdue books on page load
  useEffect(() => {
    fetchMyBooks();
    fetchOverdueBooks();
  }, []);

  // Fetch books when search changes
  useEffect(() => {
    if (search.trim() === "") {
      setBooks([]);
      return;
    }
    fetchBooks();
  }, [search]);

  /** 📌 API: Search books by title/author/isbn */
  const fetchBooks = async () => {
    try {
      const res = await api.get<Book[]>(`/books/search?q=${search}`);
      setBooks(res.data);
    } catch (err) {
      console.error("Error fetching books:", err);
      setBooks([]);
    }
  };

  /** 📌 API: Borrow a book */
  const handleBorrow = async (bookId: number) => {
    try {
      await api.post(
        "/user/borrow",
        { book_id: bookId },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      alert(" Book borrowed successfully!");
      fetchMyBooks(); // refresh borrowed list
    } catch (err) {
      console.error("Failed to borrow:", err);
      alert(
        " Borrow failed. You may have reached the limit or book unavailable."
      );
    }
  };

  /**  API: Fetch borrowed books */
  const fetchMyBooks = async () => {
    try {
      const res = await api.get<BorrowedBook[]>("/user/mybooks", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setBorrowedBooks(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch borrowed books.");
    }
  };

  /**  API: Fetch overdue books */
  const fetchOverdueBooks = async () => {
    try {
      const res = await api.get<OverdueBook[]>("/user/mybooks/overdue", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setOverdueBooks(res.data);
      console.log("Overdue books from API:", res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch overdue books.");
    }
  };

  /**  API: Return a book by ISBN */
  const handleReturn = async (isbn: string) => {
    try {
      console.log(`Returning book with ISBN: ${isbn}`);
      const response = await api.post(`/user/return/${isbn}`, null, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      console.log(" Book status:", response.data);
      alert("Book returned successfully!");
      fetchMyBooks(); // Refresh borrowed books list
    } catch (err) {
      console.error("Failed to return book:", err);
      alert("Failed to return book.");
    }
  };

  return (
    <div className="center" style={{ padding: "2rem" }}>
      <h1>📚 User Dashboard</h1>

      {/* Search Section */}
      <div style={{ marginBottom: "2rem" }}>
        <h2>Search Books</h2>
        <input
          className="input"
          type="text"
          placeholder="Search by title/author/isbn..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ width: "300px", marginBottom: "1rem" }}
        />
        {books.length > 0 &&
          books.map((book) => (
            <div
              key={book.id}
              className="card"
              style={{ margin: "1rem auto", width: "300px" }}
            >
              <h3>{book.title}</h3>
              <p>
                <strong>Author:</strong> {book.author}
              </p>
              <p>
                <strong>ISBN:</strong> {book.isbn}
              </p>
              <p>
                <strong>Copies Available:</strong> {book.copies_available}
              </p>
              <button className="btn" onClick={() => handleBorrow(book.id)}>
                Borrow
              </button>
            </div>
          ))}
        {search.trim() !== "" && books.length === 0 && <p>No books found.</p>}
      </div>

      {/*  Borrowed Books Section */}
      <div style={{ marginBottom: "2rem" }}>
        <h2>My Borrowed Books</h2>
        {borrowedBooks.length === 0 ? (
          <p>You have no borrowed books.</p>
        ) : (
          borrowedBooks
            .filter((book) => !book.return_date) // only books not returned
            .map((book) => (
              <div key={book.id} className="card">
                <h3>{book.book.title}</h3>
                <p>
                  <strong>Author:</strong> {book.book.author}
                </p>
                <p>
                  <strong>ISBN:</strong> {book.book.isbn}
                </p>
                <p>
                  <strong>Borrowed:</strong> {book.borrow_date}
                </p>
                <p>
                  <strong>Due:</strong> {book.due_date}
                </p>
                <button
                  className="btn"
                  onClick={() => handleReturn(book.book.isbn.trim())}
                >
                  Return Book
                </button>
              </div>
            ))
        )}
      </div>

      {/*  Overdue Books Section */}
      <div>
        <h2 style={{ color: "red" }}>Overdue Books</h2>
        {overdueBooks.length === 0 ? (
          <p>No overdue books 🎉</p>
        ) : (
          overdueBooks.map((book) => (
            <div
              key={book.id}
              className="card"
              style={{ margin: "0.5rem auto", width: "300px" }}
            >
              <h4>{book.title}</h4>
              <p>
                Due: {book.due_date} | Overdue by {book.days_overdue} days
              </p>
            </div>
          ))
        )}
        <div>
          <LogoutButton />
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
