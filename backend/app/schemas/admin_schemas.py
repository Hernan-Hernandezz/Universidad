"""Schemas de validación para el módulo de administración."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class CrearUsuarioSchema(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    id_rol: int


class CrearAsignaturaSchema(BaseModel):
    codigo: str
    nombre_materia: str
    creditos: int = 3


class CrearClaseSchema(BaseModel):
    id_asignatura: int
    id_docente: int
    periodo_academico: str
    grupo: str = "01"
    cupo_maximo: int = 35


class CrearMatriculaSchema(BaseModel):
    id_estudiante: int
    id_clase: int


class CrearTareaSchema(BaseModel):
    id_clase: int
    creado_por: int
    titulo_tarea: str
    descripcion: Optional[str] = None
    fecha_entrega: datetime
    porcentaje_dentro_corte: float
    corte: int


class CrearAlertaSchema(BaseModel):
    id_creador: int
    titulo: str
    mensaje: str
    prioridad: str = "Media"
