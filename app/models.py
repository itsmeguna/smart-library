# app/models.py

from sqlalchemy import Column, String, Integer
from app.database import Base  

class Book(Base):
    __tablename__ = "books"  
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, default=1)
    