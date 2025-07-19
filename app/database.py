# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# ✅ Database name: no spaces allowed — change it in PostgreSQL if needed
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:new_password@localhost/smart_library"

# ✅ SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ✅ Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()

# ✅ Optional: print successful connection message
try:
   with engine.connect() as conn:
    conn.execute(text("SELECT 1"))  # ✅ Works correctly
    print("✅ Connected successfully!")
except Exception as e:
    print("❌ Failed to connect to PostgreSQL")
    print("Error:", e)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


