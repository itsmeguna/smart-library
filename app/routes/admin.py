import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BookCreate, BookOut,ActiveUserOut, MostBorrowedBook, MonthlyUsageReportItem,OverdueBookItem
from app.models import Admin
from app.auth_utils import get_current_admin
from app.crud.books_crud import create_book, get_books, delete_book
from app.crud.admin_crud import get_active_users_with_books, get_most_borrowed_books, get_active_users, get_monthly_usage_report, get_all_overdue_books
from app.auth_utils import admin_required
from typing import List


# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter(prefix="/admin", tags=["Admin Book Management"])

#  Add book
@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    new_book = create_book(db, book)
    logger.info(f"Book added by Admin {admin.name} (ISBN: {book.isbn})")
    return new_book

#  Get all books
@router.get("/books", response_model=List[BookOut], status_code=status.HTTP_200_OK)
def list_books(db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    books = get_books(db)
    logger.info(f"Books listed by Admin {admin.name}. Total: {len(books)}")
    return books

# Delete book by ISBN
@router.delete("/books/{isbn}", status_code=status.HTTP_200_OK)
def remove_book(isbn: str, db: Session = Depends(get_db), admin: Admin = Depends(get_current_admin)):
    success = delete_book(db, isbn)
    if not success:
        logger.warning(f"Delete failed by Admin {admin.name}. Book not found: ISBN {isbn}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Book deleted by Admin {admin.name}: ISBN {isbn}")
    return {"detail": f"Book with ISBN {isbn} deleted"}

# Active Users Report
@router.get("/active-users", response_model=List[ActiveUserOut], status_code=status.HTTP_200_OK)
def active_users_report(db: Session = Depends(get_db), admin: Admin = Depends(admin_required)):
    users = get_active_users(db)
    logger.info(f"Active user data: {users}")
    return users

@router.get("/most_borrowed", response_model=list[MostBorrowedBook], dependencies=[Depends(admin_required)])
def most_borrowed_books_report(db: Session = Depends(get_db)):
    books = get_most_borrowed_books(db)
    logger.info(f"Admin accessed most borrowed books report. Count: {len(books)}")
    return books

@router.get("/monthly_usage", response_model=list[MonthlyUsageReportItem], dependencies=[Depends(admin_required)])
def monthly_usage_report(
    year: int = Query(default=datetime.utcnow().year),
    month: int = Query(default=datetime.utcnow().month),
    db: Session = Depends(get_db)
):
    return get_monthly_usage_report(db, year, month)


@router.get("/overdue-books", response_model=list[OverdueBookItem], dependencies=[Depends(admin_required)])
def overdue_books_report(db: Session = Depends(get_db)):
    logger.info("Admin requested overdue books report.")
    return get_all_overdue_books(db)
