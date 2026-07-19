from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schemas import LoginSchema, TokenSchema
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenSchema)
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(datos.correo, datos.password)
