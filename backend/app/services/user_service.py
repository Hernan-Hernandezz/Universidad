"""
Módulo de servicios del usuario.

Contiene la clase User con los métodos para consultar
horarios, resumen académico y tareas pendientes.
"""

from datetime import datetime, timedelta
from icecream import ic
from app.models.models import (
    Aulas,
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
    """
    Servicio de consultas del usuario estudiante.

    Proporciona métodos para obtener horarios, resumen académico
    y tareas pendientes de un estudiante en la plataforma.
    """

    def __init__(self, db: Session, user_id: int):
        """
        Inicializa el servicio con una sesión de base de datos.

        Args:
            db: Sesión activa de SQLAlchemy para consultas a PostgreSQL.
        """
        self.db = db
        self.user_id = user_id

    def get_class_schedule(self):
        """
        Obtiene el horario semanal de un estudiante ordenado por proximidad.

        Consulta los horarios de todas las clases en las que el estudiante
        está matriculado y los ordena mostrando primero las clases más
        próximas según el día y hora actual.

        Args:
            user_id: Identificador único del estudiante.

        Returns:
            list: Lista de horarios ordenados por proximidad a la hora actual.
        """
        user_id = self.user_id
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
                Clases_Horario.id_aula,
                Aulas.id_aula,
                Aulas.numero_bloque,
                Aulas.numero_salon,
            )
            .filter(
                Matriculas.id_estudiante == user_id
                and Matriculas.id_estado_matricula == 1
            )
            .join(Usuarios, Matriculas.id_estudiante == Usuarios.id_usuario)
            .join(Clases, Matriculas.id_clase == Clases.id_clase)
            .join(Asignaturas, Clases.id_asignatura == Asignaturas.id_asignatura)
            .join(Clases_Horario, Matriculas.id_clase == Clases_Horario.id_clase)
            .join(Aulas, Clases_Horario.id_aula == Aulas.id_aula)
            .order_by(
                Clases_Horario.id_dia_semana, Clases_Horario.id_clase_horario.desc()
            )
            .all()
        )

        today = datetime.now()
        today_weekday = today.isoweekday()
        next_class = []

        def days_remaining(day):
            """
            Calcula los días restantes hasta un día de la semana dado.

            Args:
                day: Número del día de la semana (1=Lunes, 7=Domingo).

            Returns:
                int: Días restantes de forma circular (0-6).
            """
            return (day - today_weekday) % 7

        for i in query:
            if i.id_dia_semana >= today_weekday and (
                i.hora_inicio.hour >= today.time().hour
                or i.hora_fin.hour <= today.time().hour
            ):
                next_class.append(i)
            else:
                next_class.insert(0, i)
        result = []
        ic(next_class)
        for i in next_class:
            fecha_clase = today + timedelta(days=days_remaining(i.id_dia_semana))
            result.append(
                {
                    "fecha_proxima_clase": fecha_clase,
                    "hora_fin": str(i.hora_fin),
                    "hora_inicio": str(i.hora_inicio),
                    "id_dia_semana": i.id_dia_semana,
                    "id_clase_horario": i.id_clase_horario,
                    "nombre_materia": i.nombre_materia,
                    "aula": f"bloque:{i.numero_bloque} salon:{i.numero_salon}",
                }
            )
        ic(result)
        return result

    def get_academic_summary(self):
        """
        Obtiene el resumen académico de un estudiante.

        Consulta las materias inscritas del estudiante junto con
        su nota final por cada asignatura en el periodo activo.

        Args:
            user_id: Identificador único del estudiante.

        Returns:
            list: Lista con las materias y notas finales del estudiante.
        """
        user_id = self.user_id
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
            .join(Usuarios, Matriculas.id_estudiante == Usuarios.id_usuario)
            .join(Clases, Matriculas.id_clase == Clases.id_clase)
            .join(Asignaturas, Clases.id_asignatura == Asignaturas.id_asignatura)
            .all()
        )
        result = []
        for i in query:
            result.append(
                {"nombre_materia": i.nombre_materia, "nota_final": i.nota_final}
            )
        return result

    def get_pending_tasks(self):
        """
        Obtiene las tareas pendientes de un estudiante ordenadas por fecha.

        Consulta todas las tareas con estado pendiente del estudiante,
        ordenadas por fecha de entrega de más próxima a más lejana.

        Args:
            user_id: Identificador único del estudiante.

        Returns:
            list: Lista de tareas pendientes ordenadas por fecha de entrega.
        """
        user_id = self.user_id
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
            .join(Usuarios, Matriculas.id_estudiante == Usuarios.id_usuario)
            .join(Clases, Matriculas.id_clase == Clases.id_clase)
            .join(Asignaturas, Clases.id_asignatura == Asignaturas.id_asignatura)
            .join(Tareas, Tareas_Estudiante.id_tarea == Tareas.id_tarea)
            .filter(Tareas_Estudiante.id_estado_tarea == 1)
            .order_by(Tareas.fecha_entrega)
            .all()
        )
        result = []
        for i in query:
            result.append(
                {
                    "asignatura": i.nombre_materia,
                    "titulo_tarea": i.titulo_tarea,
                    "fecha_entrega": i.fecha_entrega,
                }
            )
        return result

    def get_class_user(self, user_id: int, db: Session):
        """
        Obtiene todas las clases en las que está matriculado un estudiante.

        Args:
            user_id: Identificador único del estudiante.
            db: Sesión activa de SQLAlchemy.

        Returns:
            list: Lista de matrículas del estudiante.
        """
        clases_estudiante = (
            db.query(Matriculas).filter(Matriculas.id_estudiante == user_id).all()
        )
        return clases_estudiante

    def get_user_id(self, user_id: int, db: Session):
        """
        Obtiene la información completa de un usuario por su identificador.

        Args:
            user_id: Identificador único del usuario.
            db: Sesión activa de SQLAlchemy.

        Returns:
            Usuarios: Objeto con todos los datos del usuario, o None si no existe.
        """
        user = db.query(Usuarios).filter(Usuarios.id_usuario == user_id).first()
        return user
