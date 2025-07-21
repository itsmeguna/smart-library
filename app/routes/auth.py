from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth_utils import create_access_token, get_current_admin
from app.database import get_db
from datetime import datetime,timedelta

import logging

from app import models, schemas, database, auth_utils
from app.auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="", tags=["Authentication"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#------------------Admin Authentication Routes------------------#
# 🔐 Admin Registration
@router.post("/admin/register", response_model=schemas.AdminOut)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth_utils.hash_password(admin.password)
    new_admin = models.Admin(name=admin.name, email=admin.email, password=hashed_pw)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    logger.info(f"✅ Admin registered: {new_admin.name} ({new_admin.email})")
    return new_admin


# 🔐 Admin Login
@router.post("/admin/login") 
def login_admin(login_data: schemas.AdminLogin, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == login_data.email).first()

    if not admin or not auth_utils.verify_password(login_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this resource...you need to be an admin",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"admin_id": admin.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    logger.info(f"✅ Admin login: {admin.name} (ID={admin.id})")  
    return {"access_token": access_token, "token_type": "bearer"}


# 🧪 Optional Swagger /token endpoint for Swagger UI
@router.post("/admin/token")
def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == form_data.username).first()

    if not admin or not auth_utils.verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"admin_id": admin.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

# 🔐 Test Route (protected)
@router.get("/admin/whoami")
def protected_admin_route(current_admin: models.Admin = Depends(auth_utils.get_current_admin)):
    return {"message": f"Hello Admin, {current_admin.name}!"}

#------------------User Authentication Routes------------------#
@router.post("/users/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth_utils.hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/users/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth_utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth_utils.create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}