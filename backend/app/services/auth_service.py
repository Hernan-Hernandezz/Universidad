from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from icecream import ic
import os

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


class AuthService:
    payload = {}

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, mail: str):
        user = (
            self.db.query(models.Usuarios)
            .filter(models.Usuarios.correo == mail)
            .first()
        )
        return user

    def verify_password(self, password: str, hash):
        return pwd_context.verify(password, hash)

    def crear_token(self, data: dict):
        datos = data.copy()
        expiracion = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        datos.update({"exp": expiracion})
        return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

    def login(self, mail: str, password: str):
        user = self.get_user(mail)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Usuario o contraseña incorrecta"
            )

        # este verificaba si la contraseña estaba en hash
        if not self.verify_password(password, user.contrasena_hash):
            raise HTTPException(status_code=401, detail="contraseña incorrecta")
        token = self.crear_token(
            {"id": user.id_usuario, "correo": user.correo, "rol": user.id_rol}
        )
        ic.disable()
        ic(token)
        return {"access_token": token, "token_type": "bearer"}

    def verify_token(self, token):
        ic.enable()
        ic("entro a verificar token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            ic(payload)
            return True
        except JWTError:
            raise HTTPException(status_code=401, detail="token invalido")


# obtiene toda la informacion del usuario por id
def get_user_id(user_id: int, db: Session):
    user: models.Usuarios = (
        db.query(models.Usuarios).filter(models.Usuarios.id_usuario == user_id).first()
    )
    return user


# obtiene toda la informacion de la clase por id
def get_class_id(class_id: int, db: Session):
    classId = (
        db.query(models.Clases).filter(models.Clases.id_asignatura == class_id).first
    )
    return classId


# obtiene toda la clases del usuario con su id
def get_class_user(user_id: int, db: Session):
    clases_estudiante = (
        db.query(models.Matriculas)
        .filter(models.Matriculas.id_estudiante == user_id)
        .all()
    )
    return clases_estudiante
