from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ PostgreSQL URL Format: "postgresql://user:password@host:port/dbname"
DATABASE_URL = "postgresql://postgres:FF66fK0=@localhost:5432/smart_library"  # update if needed

# 🔌 Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# 🧵 Create a DB session factory (used in routes & CRUD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🏗️ Base class for your models (used in models.py)
Base = declarative_base()

# ✅ Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  # give control to route
    finally:
        db.close()
