from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base  

Base = declarative_base()

# Admin Table
class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default= (text('now()')), nullable=False)


# Book Table

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    copies_available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #borrowed_records = relationship("BorrowedBook", back_populates="book")

    
# User Table (students & faculty only)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(20), nullable=False)  # 'student' or 'faculty'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    borrowed_books = relationship("BorrowedBook", back_populates="user")


# Borrowed Books Table

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    isbn = Column(String, ForeignKey('books.isbn'), nullable=False) 
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", foreign_keys=[book_id])


print("✅ models.py executed")
print("✅ Tables in Base.metadata:", Base.metadata.tables.keys())
