from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import BorrowRequest, BorrowedBookOut, OverdueBookOut
from app.database import SessionLocal, engine, Base,get_db
from app.auth_utils import get_current_user
from app.crud import user_crud
from app.models import User
from typing import List


router = APIRouter(prefix="/user", tags=["Users"])

"""def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()"""

@router.post("/borrow", response_model=BorrowedBookOut)
def borrow_book(
    req: BorrowRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return user_crud.borrow_book(db, user_id=current_user["id"], book_id=req.book_id)


@router.post("/return/{isbn}",response_model=BorrowedBookOut)
def return_book_route(isbn: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.return_book(db, current_user["id"], isbn)

@router.get("/mybooks",response_model=List[BorrowedBookOut])
def get_my_borrowed_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_user_borrowed_books(db, current_user["id"])

@router.get("/mybooks/overdue",response_model=List[OverdueBookOut])
def get_my_overdue_books(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.check_overdue_books(db, current_user["id"])

