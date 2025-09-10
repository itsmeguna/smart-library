// src/pages/BookSearch.tsx
import { useEffect, useState } from "react";
import type { Book } from "../types";
import api from "../axios"; // Axios instance

export default function BookSearch() {
  // Search term entered by the user
  const [search, setSearch] = useState("");

  // Books fetched from backend
  const [books, setBooks] = useState<Book[]>([]);

  // Get role from localStorage ("admin" or "user")
  const role = localStorage.getItem("role");

  /**
   * Runs whenever the search input changes.
   * Calls the backend to get matching books.
   */
  useEffect(() => {
    if (search.trim() === "") {
      setBooks([]); // clear when empty
      return;
    }

    const fetchBooks = async () => {
      try {
        console.log(` Searching for books: ${search}`);
        const response = await api.get<Book[]>(`/books/search?q=${search}`);
        console.log(" Books fetched:", response.data);
        setBooks(response.data);
      } catch (error) {
        console.error(" Error fetching books:", error);
        setBooks([]);
      }
    };

    fetchBooks();
  }, [search]);

  /**
   * Handles borrowing a book (only for "user" role)
   */
  const handleBorrow = async (bookId: number) => {
    try {
      console.log(` Sending borrow request for book ID: ${bookId}`);

      await api.post(
        "/user/borrow",
        { book_id: bookId }, // Request body
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Send JWT
          },
        }
      );

      alert(" Book borrowed successfully!");
    } catch (err) {
      console.error(" Failed to borrow book:", err);
      alert(
        " Borrow failed. You may have reached your limit or the book is unavailable."
      );
    }
  };

  return (
    <div className="center" style={{ padding: "2rem" }}>
      <h1>📚 Book Search</h1>

      {/* Search box */}
      <input
        className="input"
        type="text"
        placeholder="Search by title, author, or ISBN..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ width: "300px", marginBottom: "1rem" }}
      />

      {/* Book results */}
      {search.trim() !== "" && books.length > 0 && (
        <>
          {books.map((book) => (
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

              {/* Borrow button only for non-admin users */}
              {role === "user" && (
                <button
                  className="btn"
                  style={{ marginTop: "0.5rem" }}
                  onClick={() => handleBorrow(book.id)}
                >
                  Borrow
                </button>
              )}
            </div>
          ))}
        </>
      )}

      {/* No results */}
      {search.trim() !== "" && books.length === 0 && <p>No books found.</p>}
    </div>
  );
}
