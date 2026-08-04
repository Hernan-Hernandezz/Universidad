"""
Módulo de autenticación.

Contiene el servicio de autenticación con métodos para verificar
credenciales, generar y validar tokens JWT.
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from icecream import ic
import os

from app.schemas.auth_schemas import TokenDataSchema, TokenSchema

pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


class AuthService:
    """
    Servicio de autenticación de la plataforma estudiantil.

    Maneja el inicio de sesión, verificación de contraseñas
    y generación y validación de tokens JWT.
    """

    payload = {}

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión activa de SQLAlchemy para consultas a PostgreSQL.
        """
        self.db = db

    def get_user(self, mail: str):
        """
        Busca un usuario en la base de datos por su correo.

        Args:
            mail: Correo electrónico del usuario.

        Returns:
            Usuarios: Objeto del usuario si existe, None si no se encuentra.
        """
        user = (
            self.db.query(models.Usuarios)
            .filter(models.Usuarios.correo == mail)
            .first()
        )
        return user

    def verify_password(self, password: str, hash: str):
        """
        Verifica que una contraseña en texto plano coincida con su hash.

        Args:
            password: Contraseña en texto plano ingresada por el usuario.
            hash: Hash de la contraseña almacenado en la base de datos.

        Returns:
            bool: True si la contraseña es correcta, False si no coincide.
        """
        return pwd_context.verify(password, hash)

    def crear_token(self, data: dict):
        """
        Genera un token JWT con los datos del usuario.

        Agrega automáticamente la fecha de expiración al token
        según el valor de EXPIRE_MINUTES.

        Args:
            data: Diccionario con los datos a incluir en el token.
                  Ejemplo: {"id": 1, "correo": "carlos@edu.com", "rol": 1}

        Returns:
            str: Token JWT codificado y firmado.
        """
        datos = data.copy()
        expiracion = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        datos.update({"exp": expiracion})
        return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

    def login(self, mail: str, password: str):
        """
        Autentica un usuario y retorna un token JWT.

        Verifica que el usuario exista y que la contraseña sea correcta.
        Si las credenciales son válidas genera y retorna un token de acceso.

        Args:
            mail: Correo electrónico del usuario.
            password: Contraseña en texto plano.

        Returns:
            dict: Diccionario con access_token y token_type.

        Raises:
            HTTPException: 401 si el usuario no existe o la contraseña es incorrecta.
        """
        user = self.get_user(mail)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Usuario o contraseña incorrecta"
            )
        if not self.verify_password(password, user.contrasena_hash):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        token = self.crear_token(
            {"id": user.id_usuario, "correo": user.correo, "rol": user.id_rol}
        )
        return {"access_token": token, "token_type": "bearer"}

    def verify_token(self, token: str):
        """
        Verifica que un token JWT sea válido.

        Decodifica el token usando la SECRET_KEY y verifica
        que no haya expirado ni sido modificado.

        Args:
            token: Token JWT a verificar.

        Returns:
            bool: payload si el token es válido.

        Raises:
            HTTPException: 401 si el token es inválido o ha expirado.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return TokenDataSchema(
                id=payload["id"], correo=payload["correo"], rol=payload["rol"]
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")


def get_class_id(class_id: int, db: Session):
    """
    Obtiene la información de una clase por su identificador.

    Args:
        class_id: Identificador único de la asignatura.
        db: Sesión activa de SQLAlchemy.

    Returns:
        Clases: Objeto con los datos de la clase, o None si no existe.
    """
    classId = (
        db.query(models.Clases).filter(models.Clases.id_asignatura == class_id).first()
    )
    return classId
