# main.py
from fastapi import FastAPI
from httpcore import Origin
from app.database import  engine, Base
from .routers import books


from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)  # Auto-create tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)

