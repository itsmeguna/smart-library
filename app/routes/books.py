
from fastapi import APIRouter, FastAPI, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.crud import books_crud
from app.database import SessionLocal, engine, Base,get_db
from app import  schemas
from typing import List
from sqlalchemy.exc import SQLAlchemyError
import traceback

router = APIRouter(
    tags=['Inventory']
)
@router.post("/books", response_model=List[schemas.BookOut])
def add_books(books: List[schemas.BookCreate], db: Session = Depends(get_db)):
    return books_crud.create_book(db, books)

# ✅ Get All Books
@router.get("/books", response_model=List[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    try:
        return books_crud.get_books(db)
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to retrieve books.")

# ✅ Delete a Book by ISBN
@router.delete("/books/{isbn}")
def delete(isbn: str, db: Session = Depends(get_db)):
    try:
        success = books_crud.delete_book(db, isbn)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found.")
        return {"message": f"Book with ISBN {isbn} deleted successfully!"}
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to delete book.")

# ✅ Search Book by Title, Author or ISBN
@router.get("/books/search", response_model=List[schemas.BookOut])
def search_books(q: str = Query(..., description="Search by title, author, or ISBN"),
                 db: Session = Depends(get_db)):
    try:
        result = books_crud.search_books(db, q)
        if not result:
            raise HTTPException(status_code=404, detail="No books found.")
        return result
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to search books.")

# ✅ Update Book by ISBN
@router.put("/books/{isbn}", response_model=schemas.BookOut)
def update_book_route(isbn: str, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    try:
        updated_book = books_crud.update_book(db, isbn, book)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found.")
        return updated_book
    except SQLAlchemyError:
        print (traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update book.")