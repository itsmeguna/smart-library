from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
from app.database import get_db
from app.models import Admin  

# JWT Settings
SECRET_KEY = "mysecret"  # 🔐 Replace with env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# Security schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token") # 
manual_bearer = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str: #to convert password to hash
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: #to verify plain password in database with hashed password
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str: #to create access token with expiration
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict: #to decode access token when user tries to access protected routes
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print("JWT Decode Error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ✅ For protected endpoints
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Admin: #to get current admin from token
    payload = decode_access_token(token)
    admin_id: int = payload.get("admin_id")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Token missing admin_id")
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found....you need to be an admin")
    return admin

# ✅ For Swagger or manual Bearer
def get_current_admin_from_bearer(
    credentials: HTTPAuthorizationCredentials = Security(manual_bearer),
    db: Session = Depends(get_db)
) -> Admin:
    token = credentials.credentials
    payload = decode_access_token(token)
    admin_id: int = payload.get("admin_id")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Token missing admin_id")
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin

def admin_required(current_admin: models.Admin = Depends(get_current_admin)): #to ensure the user is an admin
    if not current_admin:
        raise HTTPException(status_code=401, detail="Admin access required")
    return current_admin
#------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        role = payload.get("role")
        return {"id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

