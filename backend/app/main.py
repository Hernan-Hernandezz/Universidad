from app import schemas
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app.models import models
from app.routes import auth
from app.schemas.user_schemas import (
    AcademicSummarySchema,
    ClassScheduleSchema,
    PendingTasks,
    UserIdSchema,
)
from app.services.auth_service import get_user_id, get_class_user
from typing import List
from app.services.user_service import User

# from app.config import setup_icecream
#
# setup_icecream()

Base.metadata.create_all(bind=engine)
db: Session = Depends(get_db)
app = FastAPI(
    title="Plataforma Estudiantil API",
    description="Backend de la plataforma estudiantil inteligente",
    version="1.0.0",
)

router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"mensaje": "Plataforma Estudiantil API funcionando ✅"}


@app.get("/health")
def health():
    return {"estado": "ok"}


# user


@app.get("/user/{user_id}")
async def user_id(user_id: int, db: Session = Depends(get_db)):
    user: models.Usuarios = get_user_id(user_id, db)
    return user


@app.get("/user/{user_id}/class")
def class_user(user_id: int, db: Session = Depends(get_db)):
    classData = get_class_user(user_id, db)
    return classData


@app.post("/user/horarios", response_model=List[ClassScheduleSchema])
def class_schedule(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_class_schedule(datos.user_id)


@app.post("/user/academic_summary", response_model=List[AcademicSummarySchema])
def academic_summary(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_academic_summary(datos.user_id)


@app.post("/user/pending_tasks", response_model=List[PendingTasks])
def pending_tasks(datos: UserIdSchema, db: Session = Depends(get_db)):
    query = User(db)
    return query.get_pending_tasks(datos.user_id)
