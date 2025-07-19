# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # 'student' or 'faculty'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    #access_token: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    copies_available: int

    class Config:
        from_attributes = True  # formerly orm_mode


class BorrowRequest(BaseModel):
    book_id: int

class BorrowedBookOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    isbn: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class BorrowedBookInfo(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class ReturnBookRequest(BaseModel):
    user_id: int
    isbn: str


class ReturnBookResponse(BaseModel):
    message: str


class OverdueBookOut(BaseModel):
    id: int
    book: BookOut
    due_date: datetime
    days_overdue: int

    class Config:
        from_attributes = True

#class ReturnBookResponse(BaseModel):
#    message: str