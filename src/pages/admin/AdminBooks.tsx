// src/pages/admin/AdminBooks.tsx
import { useState } from "react";
import api from "../../axios";
import type { Book } from "../../types";

export default function AdminBooks() {
  const [showBookModal, setShowBookModal] = useState(false);
  const [bookSearch, setBookSearch] = useState("");
  const [books, setBooks] = useState<Book[]>([]);
  const [bookForm, setBookForm] = useState({
    title: "",
    author: "",
    isbn: "",
    copies_available: 0,
  });

  const authHeaders = {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };

  // Search books
  const handleBookSearch = async (query: string) => {
    setBookSearch(query);
    if (!query.trim()) {
      setBooks([]);
      return;
    }
    try {
      const res = await api.get(`/books/search?q=${query}`, {
        headers: authHeaders,
      });
      setBooks(res.data);
    } catch (err) {
      console.error("Search failed", err);
      setBooks([]);
    }
  };

  // Add book
  const handleAddBook = async () => {
    try {
      await api.post("/admin/books", [bookForm], { headers: authHeaders });
      alert("Book added successfully");
      setShowBookModal(false);
      setBookForm({ title: "", author: "", isbn: "", copies_available: 0 });
      setBooks([]); // Clear search results
    } catch (err) {
      console.error("Add book failed", err);
      alert("Failed to add book");
    }
  };

  // Delete book
  const handleDeleteBook = async (isbn: string) => {
    if (!window.confirm("Are you sure you want to delete this book?")) return;
    try {
      await api.delete(`/admin/books/${isbn}`, { headers: authHeaders });
      alert("Book deleted");
      setBooks((prev) => prev.filter((b) => b.isbn !== isbn));
    } catch (err) {
      console.error("Delete failed", err);
      alert("Failed to delete book");
    }
  };

  return (
    <section>
      <h2>📚 Manage Books</h2>

      {/* Top bar */}
      <div style={{ display: "flex", gap: "2rem", marginBottom: "3rem" }}>
        <button className="btn" onClick={() => setShowBookModal(true)}>
          Add Book
        </button>
        <input
          type="text"
          placeholder="Search by title/author/isbn..."
          value={bookSearch}
          onChange={(e) => handleBookSearch(e.target.value)}
          style={{ flex: 1 }}
        />
      </div>

      {/* Search results */}
      {books.length === 0 && bookSearch.trim() && <p>No books found.</p>}
      {books.map((book) => (
        <div key={book.id} className="card" style={{ margin: "0.5rem 0" }}>
          <strong>{book.title}</strong> by {book.author} (ISBN: {book.isbn}) —
          Copies: {book.copies_available}
          <button
            onClick={() => handleDeleteBook(book.isbn)}
            style={{
              marginLeft: "1rem",
              background: "red",
              color: "white",
            }}
          >
            Delete
          </button>
        </div>
      ))}

      {/* Add Book Modal */}
      {showBookModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Add New Book</h3>
            <input
              placeholder="Title"
              value={bookForm.title}
              onChange={(e) =>
                setBookForm({ ...bookForm, title: e.target.value })
              }
            />
            <input
              placeholder="Author"
              value={bookForm.author}
              onChange={(e) =>
                setBookForm({ ...bookForm, author: e.target.value })
              }
            />
            <input
              placeholder="ISBN"
              value={bookForm.isbn}
              onChange={(e) =>
                setBookForm({ ...bookForm, isbn: e.target.value })
              }
            />
            <input
              type="number"
              placeholder="Copies Available"
              value={bookForm.copies_available}
              onChange={(e) =>
                setBookForm({
                  ...bookForm,
                  copies_available: Number(e.target.value),
                })
              }
            />
            <div style={{ marginTop: "1rem" }}>
              <button className="btn" onClick={handleAddBook}>
                Save
              </button>
              <button
                onClick={() => setShowBookModal(false)}
                style={{ marginLeft: "1rem" }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
<style>{`
      .modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
      }
      .modal {
        background: white;
        padding: 2rem;
        border-radius: 6px;
        width: 400px;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
        .modal input {
        padding: 0.6rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        width: 100%;
      }

    `}</style>;
