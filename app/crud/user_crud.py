from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models
from app.models import Book, BorrowedBook
from datetime import datetime, timezone



def borrow_book(db: Session, user_id: int, book_id: int):
    # 1. Getting book
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.copies_available < 1:
        raise HTTPException(status_code=400, detail="No copies available")

    # 2. Checking limit
    active_borrows = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.user_id == user_id,
        models.BorrowedBook.return_date == None
    ).count()
    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Borrowing limit reached")

    # 3. Check for overdue
    overdue = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.user_id == user_id,
        models.BorrowedBook.return_date == None,
        models.BorrowedBook.due_date < datetime.utcnow()
    ).first()
    if overdue:
        raise HTTPException(status_code=403, detail="You have overdue books")

    # 4. Create borrow entry
    due_date = datetime.utcnow() + timedelta(days=14)
    borrow = models.BorrowedBook(
        user_id=user_id,
        book_id=book_id,
        isbn=book.isbn,
        borrow_date=datetime.utcnow(),
        due_date=due_date
    )
    db.add(borrow)

    # 5. Update book copies
    book.copies_available -= 1

    db.commit()
    db.refresh(borrow)
    return borrow


def return_book(db: Session, user_id: int, isbn: str):
    borrow = (
        db.query(BorrowedBook)
        .join(Book, BorrowedBook.book_id == Book.id)
        .filter(
            BorrowedBook.user_id == user_id,
            Book.isbn == isbn,
            BorrowedBook.return_date.is_(None)
        )
        .first()
    )
    if not borrow:
        raise HTTPException(status_code=404, detail="No active borrow record found for this book.")

    borrow.return_date = datetime.utcnow()
    borrow.book.copies_available += 1
    db.commit()
    db.refresh(borrow)
    return borrow #{"message": "Book returned successfully."}



def get_user_borrowed_books(db: Session, user_id: int):
    borrows = (
        db.query(BorrowedBook)
        .filter(BorrowedBook.user_id == user_id)
        .all()
    )
    return borrows



from datetime import datetime

def check_overdue_books(db: Session, user_id: int):
    overdue = (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.user_id == user_id,
            BorrowedBook.return_date.is_(None),
            BorrowedBook.due_date < datetime.now(timezone.utc)
        )
        .all()
    )
    now = datetime.now(timezone.utc)  # aware datetime in UTC

    
    result = []
    for borrow in overdue:
        days_overdue = (now - borrow.due_date).days
        result.append({
            "id": borrow.id,
            "book": borrow.book,  # This is a Book model instance, Pydantic will convert using BookOut
            "due_date": borrow.due_date,
            "days_overdue": days_overdue,
        })
    return result
    #return overdue
