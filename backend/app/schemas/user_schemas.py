import datetime
from pydantic import BaseModel, EmailStr
from datetime import time, datetime


class ClassScheduleSchema(BaseModel):
    fecha_proxima_clase: datetime
    hora_fin: time
    hora_inicio: time
    id_dia_semana: int
    id_clase_horario: int
    nombre_materia: str
    aula: str

    class Config:
        from_attributes = True


class AcademicSummarySchema(BaseModel):
    nombre_materia: str
    nota_final: float | None

    class Config:
        from_attributes = True


class PendingTasks(BaseModel):
    asignatura: str
    titulo_tarea: str
    fecha_entrega: datetime

    class Config:
        from_attributes = True


class UserIdSchema(BaseModel):
    user_id: int


class UsuarioRespuesta(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    id_rol: int
    activo: bool
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class UsuarioActualizar(BaseModel):
    nombre: str | None = None
    correo: EmailStr | None = None
