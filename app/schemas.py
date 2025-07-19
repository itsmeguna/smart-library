from pydantic import BaseModel
from typing import Optional
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies_available: int

class BookOut(BookCreate):
    id: int

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    copies_available: Optional[int]

    class Config:
        from_attributes = True
