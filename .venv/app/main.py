# app/main.py

from fastapi import FastAPI
from app.routes import auth
from app.routes import user
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer





app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
'''
# Security scheme for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Smart Library API",
        version="1.0.0",
        description="API for managing book borrow and return system with JWT authentication.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema '''

#app.openapi = custom_openapi