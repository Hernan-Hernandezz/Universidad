from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app.routes import auth, user

from app.config import setup_icecream

setup_icecream()

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
app.include_router(user.router)


@app.get("/")
def root():
    return {"mensaje": "Plataforma Estudiantil API funcionando ✅"}


@app.get("/health")
def health():
    return {"estado": "ok"}
