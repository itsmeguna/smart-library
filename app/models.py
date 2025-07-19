from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func,Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"  # ✅ use lowercase convention

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, default=1)



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(20), nullable=False)  # For student or fac
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #Borrowed_book = Column(String, nullable=True)
    
    borrowed_books = relationship("BorrowedBook", back_populates="user")

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)  # Check with Naveen for Books table
    isbn = Column(String, ForeignKey('books.isbn'), nullable=False)
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", foreign_keys=[book_id])