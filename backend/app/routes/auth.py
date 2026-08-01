from icecream import ic
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schemas import (
    LoginSchema,
    TokenSchema,
    TokenVerifySchema,
    TokenDataSchema,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenSchema)
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(datos.mail, datos.password)


@router.post("/token")
def token(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    service = AuthService(db)
    ic(f"el token es:{datos.access_token}")
    return service.verify_token(datos.access_token)
