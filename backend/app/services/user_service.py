from datetime import datetime, timedelta
from icecream import ic
from app.models.models import (
    Tareas_Estudiante,
    Matriculas,
    Usuarios,
    Asignaturas,
    Clases,
    Clases_Horario,
    Tareas,
)
from sqlalchemy.orm import Session


class User:
    def __init__(self, db: Session):
        self.db = db

    # horarios de clase
    def get_class_schedule(self, user_id: int):
        self.user_id = user_id
        query = (
            self.db.query(
                Matriculas.id_estudiante,
                Usuarios.nombre,
                Usuarios.correo,
                Asignaturas.nombre_materia,
                Clases_Horario.id_clase_horario,
                Clases_Horario.id_dia_semana,
                Clases_Horario.hora_inicio,
                Clases_Horario.hora_fin,
            )
            .filter(
                Matriculas.id_estudiante == user_id
                and Matriculas.id_estado_matricula == 1
            )
            .join(
                Usuarios,
                Matriculas.id_estudiante == Usuarios.id_usuario,
            )
            .join(
                Clases,
                Matriculas.id_clase == Clases.id_clase,
            )
            .join(
                Asignaturas,
                Clases.id_asignatura == Asignaturas.id_asignatura,
            )
            .join(Clases_Horario, Matriculas.id_clase == Clases_Horario.id_clase)
            .order_by(
                Clases_Horario.id_dia_semana, Clases_Horario.id_clase_horario.desc()
            )
            .all()
        )
        today = datetime.now()
        today_weekday = today.isoweekday()
        next_class = []

        def days_remaining(day):
            return (day - today_weekday) % 7

        for i in query:
            ic(i)
            if i.id_dia_semana >= today_weekday and (
                i.hora_inicio.hour >= today.time().hour
                or i.hora_fin.hour <= today.time().hour
            ):
                next_class.insert(0, i)
            else:
                next_class.append(i)
        ic(next_class)
        return next_class

    # Resumen academico
    def get_academic_summary(self, user_id: int):
        self.user_id = user_id
        query = (
            self.db.query(
                Matriculas.id_estudiante,
                Usuarios.nombre,
                Usuarios.correo,
                Asignaturas.nombre_materia,
                Matriculas.nota_final,
            )
            .filter(
                Matriculas.id_estudiante == user_id
                and Matriculas.id_estado_matricula == 1
            )
            .join(
                Usuarios,
                Matriculas.id_estudiante == Usuarios.id_usuario,
            )
            .join(
                Clases,
                Matriculas.id_clase == Clases.id_clase,
            )
            .join(
                Asignaturas,
                Clases.id_asignatura == Asignaturas.id_asignatura,
            )
            .all()
        )
        return query

    # Tareas Pendientes
    def get_pending_tasks(self, user_id: int):
        self.user_id = user_id
        query = (
            self.db.query(
                Matriculas.id_estudiante,
                Usuarios.nombre,
                Usuarios.correo,
                Asignaturas.nombre_materia,
                Tareas.titulo_tarea,
                Tareas.fecha_entrega,
            )
            .filter(
                Matriculas.id_estudiante == user_id
                and Matriculas.id_estado_matricula == 1
            )
            .join(
                Tareas_Estudiante,
                Matriculas.id_matricula == Tareas_Estudiante.id_matricula,
            )
            .join(
                Usuarios,
                Matriculas.id_estudiante == Usuarios.id_usuario,
            )
            .join(
                Clases,
                Matriculas.id_clase == Clases.id_clase,
            )
            .join(
                Asignaturas,
                Clases.id_asignatura == Asignaturas.id_asignatura,
            )
            .join(Tareas, Tareas_Estudiante.id_tarea == Tareas.id_tarea)
            .filter(Tareas_Estudiante.id_estado_tarea == 1)
            .order_by(Tareas.fecha_entrega)
            .all()
        )
        return query
