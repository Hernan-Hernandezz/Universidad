from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    Time,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Rol(Base):
    __tablename__ = "Rol"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    usuarios = relationship("Usuarios", back_populates="rol")


class Usuarios(Base):
    __tablename__ = "Usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("Rol.id_rol"), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    actualizado_en = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    rol = relationship("Rol", back_populates="usuarios")
    sesiones = relationship("Sesiones", back_populates="usuario")
    clases_docente = relationship("Clases", back_populates="docente")
    matriculas = relationship("Matriculas", back_populates="estudiante")
    tareas_creadas = relationship("Tareas", back_populates="creador")
    alertas_creadas = relationship("Alertas", back_populates="creador")
    chats = relationship("Participante_Chat", back_populates="usuario")
    mensajes = relationship("Mensajes_Chat", back_populates="usuario")


class Sesiones(Base):
    __tablename__ = "Sesiones"
    id_sesion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    expira_en = Column(TIMESTAMP(timezone=True), nullable=False)
    usuario = relationship("Usuarios", back_populates="sesiones")


class Asignaturas(Base):
    __tablename__ = "Asignaturas"
    id_asignatura = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre_materia = Column(String(150), nullable=False)
    creditos = Column(Integer, nullable=False, default=3)
    clases = relationship("Clases", back_populates="asignatura")


class Clases(Base):
    __tablename__ = "Clases"
    id_clase = Column(Integer, primary_key=True, autoincrement=True)
    id_asignatura = Column(
        Integer, ForeignKey("Asignaturas.id_asignatura"), nullable=False
    )
    id_docente = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    periodo_academico = Column(String(10), nullable=False)
    grupo = Column(String(10), nullable=False, default="01")
    cupo_maximo = Column(Integer, nullable=False, default=35)

    asignatura = relationship("Asignaturas", back_populates="clases")
    docente = relationship("Usuarios", back_populates="clases_docente")
    matriculas = relationship("Matriculas", back_populates="clase")
    horarios = relationship("Clases_Horario", back_populates="clase")
    tareas = relationship("Tareas", back_populates="clase")


class Estado_Matricula(Base):
    __tablename__ = "Estado_Matricula"
    id_estado_matricula = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String(30), unique=True, nullable=False)
    matriculas = relationship("Matriculas", back_populates="estado_matricula")


class Matriculas(Base):
    __tablename__ = "Matriculas"
    __table_args__ = (
        UniqueConstraint(
            "id_estudiante", "id_clase", name="uq_matricula_estudiante_clase"
        ),
    )

    id_matricula = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_clase = Column(Integer, ForeignKey("Clases.id_clase"), nullable=False)
    id_estado_matricula = Column(
        Integer, ForeignKey("Estado_Matricula.id_estado_matricula"), nullable=False
    )
    nota_final = Column(Float, nullable=True)
    matriculado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())

    estudiante = relationship("Usuarios", back_populates="matriculas")
    clase = relationship("Clases", back_populates="matriculas")
    estado_matricula = relationship("Estado_Matricula", back_populates="matriculas")
    tareas = relationship("Tareas_Estudiante", back_populates="matricula")


class Aulas(Base):
    __tablename__ = "Aulas"
    id_aula = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False)
    numero_bloque = Column(String(10), nullable=False)
    numero_salon = Column(String(10), nullable=False)
    capacidad = Column(Integer, nullable=False, default=30)
    tipo = Column(String(20), nullable=False, default="salon")
    horarios = relationship("Clases_Horario", back_populates="aula")


class Dia_Semana(Base):
    __tablename__ = "Dia_Semana"
    id_dia_semana = Column(Integer, primary_key=True, autoincrement=True)
    dia = Column(String(12), nullable=False)
    horarios = relationship("Clases_Horario", back_populates="dia")


class Clases_Horario(Base):
    __tablename__ = "Clases_Horario"
    id_clase_horario = Column(Integer, primary_key=True, autoincrement=True)
    id_clase = Column(Integer, ForeignKey("Clases.id_clase"), nullable=False)
    id_aula = Column(Integer, ForeignKey("Aulas.id_aula"), nullable=False)
    id_dia_semana = Column(
        Integer, ForeignKey("Dia_Semana.id_dia_semana"), nullable=False
    )
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    clase = relationship("Clases", back_populates="horarios")
    aula = relationship("Aulas", back_populates="horarios")
    dia = relationship("Dia_Semana", back_populates="horarios")


class Estado_Tareas(Base):
    __tablename__ = "Estado_Tareas"
    id_estado_tarea = Column(Integer, primary_key=True, autoincrement=True)
    nombre_estado = Column(String(20), unique=True, nullable=False)
    tareas_estudiante = relationship("Tareas_Estudiante", back_populates="estado")


class Tareas(Base):
    __tablename__ = "Tareas"
    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    id_clase = Column(Integer, ForeignKey("Clases.id_clase"), nullable=False)
    creado_por = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    titulo_tarea = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_entrega = Column(TIMESTAMP(timezone=True), nullable=False)
    porcentaje_dentro_corte = Column(Float, nullable=False)
    corte = Column(Integer, nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())

    clase = relationship("Clases", back_populates="tareas")
    creador = relationship("Usuarios", back_populates="tareas_creadas")
    tareas_estudiante = relationship("Tareas_Estudiante", back_populates="tarea")


class Tareas_Estudiante(Base):
    __tablename__ = "Tareas_Estudiante"
    id_tarea_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    id_matricula = Column(
        Integer, ForeignKey("Matriculas.id_matricula"), nullable=False
    )
    id_tarea = Column(Integer, ForeignKey("Tareas.id_tarea"), nullable=False)
    id_estado_tarea = Column(
        Integer, ForeignKey("Estado_Tareas.id_estado_tarea"), nullable=False
    )
    nota = Column(Float, nullable=True)
    es_simulada = Column(Boolean, nullable=False, default=False)
    entregado_en = Column(TIMESTAMP(timezone=True), nullable=True)

    matricula = relationship("Matriculas", back_populates="tareas")
    tarea = relationship("Tareas", back_populates="tareas_estudiante")
    estado = relationship("Estado_Tareas", back_populates="tareas_estudiante")


class Alertas(Base):
    __tablename__ = "Alertas"
    id_alerta = Column(Integer, primary_key=True, autoincrement=True)
    id_creador = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    prioridad = Column(String(10), nullable=False, default="Media")
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())
    fecha_fin = Column(TIMESTAMP(timezone=True), nullable=True)

    creador = relationship("Usuarios", back_populates="alertas_creadas")
    estudiantes = relationship("Estudiante_Alerta", back_populates="alerta")


class Estudiante_Alerta(Base):
    __tablename__ = "Estudiante_Alerta"
    id_estudiante_alerta = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_alerta = Column(Integer, ForeignKey("Alertas.id_alerta"), nullable=False)
    leido = Column(Boolean, nullable=False, default=False)
    leido_en = Column(TIMESTAMP(timezone=True), nullable=True)
    alerta = relationship("Alertas", back_populates="estudiantes")


class Chat(Base):
    __tablename__ = "Chat"
    id_chat = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    participantes = relationship("Participante_Chat", back_populates="chat")
    mensajes = relationship("Mensajes_Chat", back_populates="chat")


class Participante_Chat(Base):
    __tablename__ = "Participante_Chat"
    id_participante = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    id_chat = Column(Integer, ForeignKey("Chat.id_chat"), nullable=False)
    unido_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    usuario = relationship("Usuarios", back_populates="chats")
    chat = relationship("Chat", back_populates="participantes")


class Mensajes_Chat(Base):
    __tablename__ = "Mensajes_Chat"
    id_mensaje = Column(Integer, primary_key=True, autoincrement=True)
    id_chat = Column(Integer, ForeignKey("Chat.id_chat"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario"), nullable=False)
    mensaje = Column(Text, nullable=False)
    es_automatico = Column(Boolean, nullable=False, default=False)
    fecha_envio = Column(TIMESTAMP(timezone=True), server_default=func.now())
    leido = Column(Boolean, nullable=False, default=False)
    chat = relationship("Chat", back_populates="mensajes")
    usuario = relationship("Usuarios", back_populates="mensajes")
