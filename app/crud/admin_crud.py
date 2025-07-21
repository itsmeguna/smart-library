# Import necessary modules and packages
import logging                            
from sqlalchemy.orm import Session         # For database session management
from app.models import User, BorrowedBook, Book  # Import ORM models
from app.schemas import ActiveUserOut      
from app import models
from sqlalchemy import func                
from datetime import datetime, timezone     
from sqlalchemy.orm import joinedload      
from typing import List, Dict              

# Configure logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level to INFO

# FUNCTION 1: Get users who have borrowed books but haven't returned them
def get_active_users(db: Session):
    logger.info("Fetching users with active borrowed books (not yet returned)...")

    try:
        # Step 1: Find unique user IDs where return_date is NULL
        active_user_ids = db.query(BorrowedBook.user_id)\
            .filter(BorrowedBook.return_date == None)\
            .distinct()\
            .all()

        logger.info(f"Found active user IDs: {[uid[0] for uid in active_user_ids]}")

        # Step 2: Extract only the IDs 
        user_ids = [uid[0] for uid in active_user_ids]

        if not user_ids:
            logger.info("No active users found.")
            return []

        # Step 3: Fetch corresponding user records
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        logger.info(f"Total active users fetched: {len(users)}")

        return users

    except Exception as e:
        logger.error(f"Error while fetching active users: {str(e)}")
        raise  # Re-raise exception to let the caller handle it

# FUNCTION 2: Load users along with their active borrowed book info using JOINs
def get_active_users_with_books(db: Session):
    # Step 1: Get all user IDs with at least one unreturned book
    active_user_ids = db.query(BorrowedBook.user_id)\
        .filter(BorrowedBook.return_date == None)\
        .distinct()\
        .all()

    user_ids = [uid[0] for uid in active_user_ids]

    # Step 2: Eager load borrowed_books and book details for performance
    users = db.query(User).options(
        joinedload(User.borrowed_books).joinedload(BorrowedBook.book)
    ).filter(User.id.in_(user_ids)).all()

    return users

# FUNCTION 3: Generate detailed report of active users with their unreturned books
def get_active_users(db: Session):
    users = get_active_users_with_books(db)
    logger.info(f"Found {len(users)} users with active borrowed books")

    response = []

    for user in users:
        borrowed_books = []

        for bb in user.borrowed_books:
            if bb.return_date is None:
                logger.debug(f"User {user.name} has active borrowed book '{bb.book.title}'")
                # Append book info only if it's not returned yet
                borrowed_books.append({
                    "title": bb.book.title,
                    "borrow_date": bb.borrow_date,
                    "due_date": bb.due_date,
                    "return_date": bb.return_date  # Should be None here
                })

        # Only include users who have active borrowed books
        if borrowed_books:
            logger.info(f"User {user.name} included in active user report with {len(borrowed_books)} books")

            response.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                # Optional: include 'role' only if the User model has it
                 "role": user.role,
                "borrowed_books": borrowed_books
            })

    logger.info("Active users report generation complete")
    return response

# FUNCTION 4: Generate a list of most borrowed books, limited by `limit`
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
        .join(models.BorrowedBook, models.Book.id == models.BorrowedBook.book_id)  # Join Book and BorrowedBook
        .group_by(models.Book.id)  # Group by each book
        .order_by(func.count(models.BorrowedBook.id).desc())  # Sort by borrow count descending
        .limit(limit)  # Limit to top N
        .all()
    )

    logger.info(f"Most borrowed books report generated. Count: {len(results)}")
    return results

# FUNCTION 5: Generate monthly usage report showing borrowed books within a specific month
def get_monthly_usage_report(db: Session, year: int, month: int):
    now = datetime.utcnow().replace(tzinfo=None)  # Current time without timezone

    print("NOW:", now, "tzinfo:", now.tzinfo)  # Debug print

    # Calculate date range of the month
    start_of_month = datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime(year + 1, 1, 1)
    else:
        end_of_month = datetime(year, month + 1, 1)

    # Get borrow records between start and end of the month
    borrowed = db.query(BorrowedBook).filter(
        BorrowedBook.borrow_date >= start_of_month,
        BorrowedBook.borrow_date < end_of_month
    ).all()

    report = []

    for entry in borrowed:
        book = entry.book
        user = entry.user

        # Convert due date to naive datetime for comparison
        due_date_naive = entry.due_date.replace(tzinfo=None) if entry.due_date else None

        # Check if overdue: not returned and past due date
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

# FUNCTION 6: Get all books that are overdue (due date passed and not returned)
def get_all_overdue_books(db: Session):
    now = datetime.utcnow()  # Current time in UTC

    # Query books where return_date is NULL and due_date is earlier than now
    overdue_entries = db.query(BorrowedBook).filter(
        BorrowedBook.return_date == None,
        BorrowedBook.due_date < now
    ).all()

    logger.info(f"Found {len(overdue_entries)} overdue books.")

    # Return list of overdue book info
    return [{
        "book_title": entry.book.title,
        "user_name": entry.user.name,
        "email": entry.user.email,
        "borrow_date": entry.borrow_date,
        "due_date": entry.due_date,
        "overdue": datetime.now(timezone.utc) > entry.due_date  # Check overdue again with timezone-aware comparison
    } for entry in overdue_entries]

def get_all_users(db: Session):
    return db.query(User).all()