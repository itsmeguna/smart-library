import logging
from sqlalchemy.orm import Session
from app.models import User, BorrowedBook,Book
from app.schemas import ActiveUserOut
from app import models
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import joinedload
from typing import List, Dict



# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_active_users(db: Session):
    logger.info("Fetching users with active borrowed books (not yet returned)...")

    try:
        # Step 1: Find user IDs with unreturned books
        active_user_ids = db.query(BorrowedBook.user_id)\
            .filter(BorrowedBook.return_date == None)\
            .distinct()\
            .all()

        logger.info(f"Found active user IDs: {[uid[0] for uid in active_user_ids]}")

        # Step 2: Extract IDs from query result
        user_ids = [uid[0] for uid in active_user_ids]

        if not user_ids:
            logger.info("No active users found.")
            return []

        # Step 3: Fetch User records
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        logger.info(f"Total active users fetched: {len(users)}")

        return users

    except Exception as e:
        logger.error(f"Error while fetching active users: {str(e)}")
        raise

def get_active_users_with_books(db: Session):
    # Get user IDs with unreturned books
    active_user_ids = db.query(BorrowedBook.user_id)\
        .filter(BorrowedBook.return_date == None)\
        .distinct()\
        .all()

    user_ids = [uid[0] for uid in active_user_ids]

    # Load users with borrowed books and their linked book titles
    users = db.query(User).options(
        joinedload(User.borrowed_books).joinedload(BorrowedBook.book)
    ).filter(User.id.in_(user_ids)).all()

    return users
def get_active_users(db: Session):
    users = get_active_users_with_books(db)
    logger.info(f"Found {len(users)} users with active borrowed books")

    response = []
    for user in users:
        borrowed_books = []
        for bb in user.borrowed_books:
            if bb.return_date is None:
                logger.debug(f"User {user.name} has active borrowed book '{bb.book.title}'")
                borrowed_books.append({
                    "title": bb.book.title,
                    "borrow_date": bb.borrow_date,
                    "due_date": bb.due_date,
                    "return_date": bb.return_date
                })

        if borrowed_books:
            logger.info(f"User {user.name} included in active user report with {len(borrowed_books)} books")

            response.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                # Uncomment this only if 'role' exists:
                 "role": user.role,
                "borrowed_books": borrowed_books
            })

    logger.info("Active users report generation complete")
    return response


def get_most_borrowed_books(db: Session, limit: int = 10):
    """
    Returns the top most borrowed books, calculated by counting borrows.
    """
    results = (
        db.query(
            Book.title,
            Book.author,
            Book.isbn,
            func.count(models.BorrowedBook.id).label("borrow_count")
        )
        .join(models.BorrowedBook, models.Book.id == models.BorrowedBook.book_id)
        .group_by(models.Book.id)
        .order_by(func.count(models.BorrowedBook.id).desc())
        .limit(limit)
        .all()
    )

    logger.info(f"Most borrowed books report generated. Count: {len(results)}")
    return results

def get_monthly_usage_report(db: Session, year: int, month: int):
    #now = datetime.utcnow()
    now = datetime.utcnow().replace(tzinfo=None)
    print("NOW:", now, "tzinfo:", now.tzinfo)


    # Start of selected month
    start_of_month = datetime(year, month, 1)

    # Start of next month for end boundary
    if month == 12:
        end_of_month = datetime(year + 1, 1, 1)
    else:
        end_of_month = datetime(year, month + 1, 1)

    borrowed = db.query(BorrowedBook).filter(
        BorrowedBook.borrow_date >= start_of_month,
        BorrowedBook.borrow_date < end_of_month
    ).all()

    report = []
    for entry in borrowed:
        book = entry.book
        user = entry.user
        due_date_naive = entry.due_date.replace(tzinfo=None) if entry.due_date else None
        overdue = (entry.return_date is None and due_date_naive < now)

        print("DUE DATE:", entry.due_date, "tzinfo:", entry.due_date.tzinfo)


        report.append({
            "book_title": book.title,
            "user_name": user.name,
            "borrow_date": entry.borrow_date,
            "return_date": entry.return_date,
            "overdue": overdue,
        })

    return report
