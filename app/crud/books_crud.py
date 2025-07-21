from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Book
from app.schemas import BookCreate, BookUpdate
from typing import List
from fastapi import HTTPException
import traceback
from app.models import User
 

def create_book(db: Session, books: List[BookCreate]):
    try:
        db_books = [Book(**book.dict()) for book in books]
        print("DEBUG:", books, type(books[0]))
        db.add_all(db_books)
        db.commit()
        for db_book in db_books:
            db.refresh(db_book)
        return db_books
    except SQLAlchemyError:
        print (traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Error while creating books.")


def get_books(db: Session) -> List[Book]:
    try:
        return db.query(Book).all()
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to retrieve books.")


def delete_book(db: Session, isbn: str):
    try:
        book = db.query(Book).filter(Book.isbn == isbn).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    except SQLAlchemyError:
        print (traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete book.")


def update_book(db: Session, old_isbn: str, book_update: BookUpdate):
    try:
        book = db.query(Book).filter(Book.isbn == old_isbn).first()
        if not book:
            return None

        update_data = book_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)
        return book
    except SQLAlchemyError:
        print (traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update book.")


def search_books(db: Session, query: str) -> List[Book]:
    try:
        search = f"%{query}%"
        return db.query(Book).filter(
            Book.title.ilike(search) |
            Book.author.ilike(search) |
            Book.isbn.ilike(search)
        ).all()
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to search books.")



