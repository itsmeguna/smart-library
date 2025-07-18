from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime



# ✅ ADMIN SCHEMAS ONLY

class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
# ─────────────────────────────────────
# User Report Schema
# ─────────────────────────────────────
# Used in monthly usage report
class MonthlyUsageOut(BaseModel):
    user_name: str
    book_title: str
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        orm_mode = True

# Used in most borrowed books report
class MostBorrowedBookOut(BaseModel):
    title: str
    author: str
    isbn: str
    borrow_count: int

class MostBorrowedBook(MostBorrowedBookOut):
    title: str
    author: str
    isbn: str
    borrow_count: int  # This is a computed field    

    class Config:
        orm_mode = True

class MonthlyUsageReportItem(BaseModel):
    book_title: str
    user_name: str
    borrow_date: datetime
    return_date: Optional[datetime]
    overdue: bool

    class Config:
        from_attributes = True
   


 #✅ ACTIVE USER SCHEMAS ONLY       
class BorrowedBookSimple(BaseModel):
    title: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]

    class Config:
        orm_mode = True

class ActiveUserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    borrowed_books: List[BorrowedBookSimple]

    class Config:
        orm_mode = True

       

# ✅ BOOK SCHEMAS ONLY

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies_available: int

class BookOut(BookCreate):
    id: int

    class Config:
        from_attributes = True