from fastapi import APIRouter, Depends
from icecream import ic
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas.user_schemas import (
    AcademicSummarySchema,
    ClassScheduleSchema,
    PendingTasks,
    UserIdSchema,
)
from app.schemas.auth_schemas import TokenVerifySchema, TokenDataSchema

from app.services.auth_service import AuthService
from typing import List
from app.services.user_service import User

router = APIRouter(prefix="/user", tags=["usuario"])


@router.get("/{user_id}")
async def user_id(user_id: int, db: Session = Depends(get_db)):
    user: models.Usuarios = get_user_id(user_id, db)
    return user


@router.get("/{user_id}/class")
def class_user(user_id: int, db: Session = Depends(get_db)):
    classData = get_class_user(user_id, db)
    return classData


@router.post(
    "/horarios"
    # , response_model=List[ClassScheduleSchema]
)
def class_schedule(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    """
    Consulta las proximas clases apartir del token.

    verifica los datos del token,
    devuelve las fechas de las proximas clases y la informacion de este

    Args:
        user_id: Identificador único del estudiante.

    Returns:
        list: Lista de proximas clases ordenadas por fecha.
    """
    token: TokenDataSchema = AuthService(db).verify_token(datos.access_token)
    user_id = token.id
    query = User(db, user_id)
    list_class = query.get_class_schedule()
    return list_class


@router.post(
    "/academic_summary"
    # , response_model=List[AcademicSummarySchema]
)
def academic_summary(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    token: TokenDataSchema = AuthService(db).verify_token(datos.access_token)
    user_id = token.id
    query = User(db, user_id)
    return query.get_academic_summary()


@router.post("/pending_tasks", response_model=List[PendingTasks])
def pending_tasks(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    """
    Consulta las tareas pendiente apartir del token.

    verifica los datos del token,

    Args:
        user_id: Identificador único del estudiante.

    Returns:
        list: Lista de tareas pendientes.
    """
    token: TokenDataSchema = AuthService(db).verify_token(datos.access_token)
    user_id = token.id
    query = User(db, user_id)
    task = query.get_pending_tasks()
    ic(task)
    return task
