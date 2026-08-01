from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas.user_schemas import (
    AcademicSummarySchema,
    ClassScheduleSchema,
    PendingTasks,
    UserIdSchema,
)
from app.services.auth_service import get_user_id, get_class_user
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


@router.post("/horarios", response_model=List[ClassScheduleSchema])
def class_schedule(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_class_schedule(datos.user_id)


@router.post("/academic_summary", response_model=List[AcademicSummarySchema])
def academic_summary(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_academic_summary(datos.user_id)


@router.post("/pending_tasks", response_model=List[PendingTasks])
def pending_tasks(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_pending_tasks(datos.user_id)
