
from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate
from typing import List

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(Book).all()

def delete_book(db:Session, isbn:str):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False




def search_books(db: Session, query: str) -> List[Book]:
    """
    Searches books by title, author, or ISBN (case-insensitive).
    """
    search = f"%{query}%"
    return db.query(Book).filter(
        Book.title.ilike(search) |
        Book.author.ilike(search) |
        Book.isbn.ilike(search)
    ).all()