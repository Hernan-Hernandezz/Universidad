"""
Módulo de rutas del administrador.

Endpoints para gestión de usuarios, materias, clases,
matrículas, tareas y alertas.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import (
    Usuarios,
    Rol,
    Asignaturas,
    Clases,
    Matriculas,
    Estado_Matricula,
    Tareas,
    Tareas_Estudiante,
    Estado_Tareas,
    Alertas,
    Estudiante_Alerta,
)
from app.schemas.admin_schemas import (
    CrearUsuarioSchema,
    CrearAsignaturaSchema,
    CrearClaseSchema,
    CrearMatriculaSchema,
    CrearTareaSchema,
    CrearAlertaSchema,
)
from app.services.auth_service import AuthService, TokenDataSchema
from app.schemas.auth_schemas import TokenVerifySchema
from typing import List

router = APIRouter(prefix="/admin", tags=["Administrador"])


def verificar_admin(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    """Verifica que el token pertenezca a un usuario con rol admin (id_rol=3)."""
    token: TokenDataSchema = AuthService(db).verify_token(datos.access_token)
    if token.rol != 3:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return token


# ─── USUARIOS ────────────────────────────────────────────────


@router.post("/usuarios")
def crear_usuario(datos: CrearUsuarioSchema, db: Session = Depends(get_db)):
    """Crea un nuevo usuario en el sistema."""
    import bcrypt

    existe = db.query(Usuarios).filter(Usuarios.correo == datos.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    hash_pw = bcrypt.hashpw(datos.contrasena.encode(), bcrypt.gensalt()).decode()
    nuevo = Usuarios(
        nombre=datos.nombre,
        correo=datos.correo,
        contrasena_hash=hash_pw,
        id_rol=datos.id_rol,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Usuario creado", "id": nuevo.id_usuario}


@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos los usuarios con su rol."""
    usuarios = (
        db.query(
            Usuarios.id_usuario,
            Usuarios.nombre,
            Usuarios.correo,
            Usuarios.activo,
            Rol.nombre.label("rol"),
        )
        .join(Rol, Usuarios.id_rol == Rol.id_rol)
        .all()
    )
    return [
        {
            "id_usuario": u.id_usuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "activo": u.activo,
            "rol": u.rol,
        }
        for u in usuarios
    ]


@router.put("/usuarios/{id_usuario}/desactivar")
def desactivar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    """Desactiva un usuario sin eliminarlo."""
    usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = False
    db.commit()
    return {"mensaje": f"Usuario {usuario.nombre} desactivado"}


@router.put("/usuarios/{id_usuario}/activar")
def activar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    """Reactiva un usuario desactivado."""
    usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = True
    db.commit()
    return {"mensaje": f"Usuario {usuario.nombre} activado"}


# ─── MATERIAS Y CLASES ────────────────────────────────────────


@router.post("/asignaturas")
def crear_asignatura(datos: CrearAsignaturaSchema, db: Session = Depends(get_db)):
    """Crea una nueva asignatura."""
    existe = db.query(Asignaturas).filter(Asignaturas.codigo == datos.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El código ya existe")
    nueva = Asignaturas(
        codigo=datos.codigo,
        nombre_materia=datos.nombre_materia,
        creditos=datos.creditos,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"mensaje": "Asignatura creada", "id": nueva.id_asignatura}


@router.get("/asignaturas")
def listar_asignaturas(db: Session = Depends(get_db)):
    """Lista todas las asignaturas."""
    return db.query(Asignaturas).all()


@router.delete("/asignaturas/{id_asignatura}")
def eliminar_asignatura(id_asignatura: int, db: Session = Depends(get_db)):
    """Elimina una asignatura si no tiene clases activas."""
    asignatura = (
        db.query(Asignaturas).filter(Asignaturas.id_asignatura == id_asignatura).first()
    )
    if not asignatura:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")
    db.delete(asignatura)
    db.commit()
    return {"mensaje": "Asignatura eliminada"}


@router.post("/clases")
def crear_clase(datos: CrearClaseSchema, db: Session = Depends(get_db)):
    """Crea una nueva clase para una asignatura."""
    nueva = Clases(
        id_asignatura=datos.id_asignatura,
        id_docente=datos.id_docente,
        periodo_academico=datos.periodo_academico,
        grupo=datos.grupo,
        cupo_maximo=datos.cupo_maximo,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"mensaje": "Clase creada", "id": nueva.id_clase}


@router.get("/clases")
def listar_clases(db: Session = Depends(get_db)):
    """Lista todas las clases con su asignatura y docente."""
    clases = (
        db.query(
            Clases.id_clase,
            Clases.periodo_academico,
            Clases.grupo,
            Clases.cupo_maximo,
            Asignaturas.nombre_materia,
            Usuarios.nombre.label("docente"),
        )
        .join(Asignaturas, Clases.id_asignatura == Asignaturas.id_asignatura)
        .join(Usuarios, Clases.id_docente == Usuarios.id_usuario)
        .all()
    )
    return [
        {
            "id_clase": c.id_clase,
            "nombre_materia": c.nombre_materia,
            "docente": c.docente,
            "periodo_academico": c.periodo_academico,
            "grupo": c.grupo,
            "cupo_maximo": c.cupo_maximo,
        }
        for c in clases
    ]


# ─── MATRÍCULAS ───────────────────────────────────────────────


@router.post("/matriculas")
def crear_matricula(datos: CrearMatriculaSchema, db: Session = Depends(get_db)):
    """Inscribe un estudiante en una clase."""
    existe = (
        db.query(Matriculas)
        .filter(
            Matriculas.id_estudiante == datos.id_estudiante,
            Matriculas.id_clase == datos.id_clase,
        )
        .first()
    )
    if existe:
        raise HTTPException(status_code=400, detail="El estudiante ya está matriculado")
    nueva = Matriculas(
        id_estudiante=datos.id_estudiante,
        id_clase=datos.id_clase,
        id_estado_matricula=1,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # asignar tareas existentes de la clase al nuevo estudiante
    tareas = db.query(Tareas).filter(Tareas.id_clase == datos.id_clase).all()
    for tarea in tareas:
        asignacion = Tareas_Estudiante(
            id_matricula=nueva.id_matricula,
            id_tarea=tarea.id_tarea,
            id_estado_tarea=1,
        )
        db.add(asignacion)
    db.commit()
    return {"mensaje": "Estudiante matriculado", "id": nueva.id_matricula}


@router.delete("/matriculas/{id_matricula}")
def cancelar_matricula(id_matricula: int, db: Session = Depends(get_db)):
    """Cancela la matrícula de un estudiante."""
    matricula = (
        db.query(Matriculas).filter(Matriculas.id_matricula == id_matricula).first()
    )
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    matricula.id_estado_matricula = 2  # Cancelada
    db.commit()
    return {"mensaje": "Matrícula cancelada"}


# ─── TAREAS Y NOTAS ───────────────────────────────────────────


@router.post("/tareas")
def crear_tarea(datos: CrearTareaSchema, db: Session = Depends(get_db)):
    """Crea una tarea y la asigna automáticamente a todos los estudiantes de la clase."""
    nueva = Tareas(
        id_clase=datos.id_clase,
        creado_por=datos.creado_por,
        titulo_tarea=datos.titulo_tarea,
        descripcion=datos.descripcion,
        fecha_entrega=datos.fecha_entrega,
        porcentaje_dentro_corte=datos.porcentaje_dentro_corte,
        corte=datos.corte,
    )
    db.add(nueva)
    db.flush()

    matriculas = (
        db.query(Matriculas)
        .filter(
            Matriculas.id_clase == datos.id_clase,
            Matriculas.id_estado_matricula == 1,
        )
        .all()
    )
    for m in matriculas:
        db.add(
            Tareas_Estudiante(
                id_matricula=m.id_matricula,
                id_tarea=nueva.id_tarea,
                id_estado_tarea=1,
            )
        )
    db.commit()
    return {"mensaje": f"Tarea creada y asignada a {len(matriculas)} estudiantes"}


@router.put("/tareas/{id_tarea_estudiante}/nota")
def calificar_tarea(
    id_tarea_estudiante: int, nota: float, db: Session = Depends(get_db)
):
    """Califica la tarea de un estudiante."""
    tarea = (
        db.query(Tareas_Estudiante)
        .filter(Tareas_Estudiante.id_tarea_estudiante == id_tarea_estudiante)
        .first()
    )
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if nota < 0 or nota > 5:
        raise HTTPException(status_code=400, detail="La nota debe estar entre 0 y 5")
    tarea.nota = nota
    tarea.id_estado_tarea = 3  # Calificado
    db.commit()
    return {"mensaje": "Nota registrada"}


@router.delete("/tareas/{id_tarea}")
def eliminar_tarea(id_tarea: int, db: Session = Depends(get_db)):
    """Elimina una tarea y todas sus asignaciones."""
    tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.query(Tareas_Estudiante).filter(Tareas_Estudiante.id_tarea == id_tarea).delete()
    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada"}


# ─── ALERTAS ─────────────────────────────────────────────────


@router.post("/alertas")
def crear_alerta(datos: CrearAlertaSchema, db: Session = Depends(get_db)):
    """Crea una alerta y la envía a todos los estudiantes activos."""
    nueva = Alertas(
        id_creador=datos.id_creador,
        titulo=datos.titulo,
        mensaje=datos.mensaje,
        prioridad=datos.prioridad,
    )
    db.add(nueva)
    db.flush()

    estudiantes = (
        db.query(Usuarios).filter(Usuarios.id_rol == 1, Usuarios.activo == True).all()
    )
    for est in estudiantes:
        db.add(
            Estudiante_Alerta(
                id_estudiante=est.id_usuario,
                id_alerta=nueva.id_alerta,
            )
        )
    db.commit()
    return {"mensaje": f"Alerta enviada a {len(estudiantes)} estudiantes"}


@router.get("/alertas")
def listar_alertas(db: Session = Depends(get_db)):
    """Lista todas las alertas creadas."""
    return db.query(Alertas).order_by(Alertas.fecha_creacion.desc()).all()


@router.delete("/alertas/{id_alerta}")
def eliminar_alerta(id_alerta: int, db: Session = Depends(get_db)):
    """Elimina una alerta y sus registros de estudiantes."""
    alerta = db.query(Alertas).filter(Alertas.id_alerta == id_alerta).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    db.query(Estudiante_Alerta).filter(
        Estudiante_Alerta.id_alerta == id_alerta
    ).delete()
    db.delete(alerta)
    db.commit()
    return {"mensaje": "Alerta eliminada"}


@router.post("/usuarios/lista")
def listar_usuarios(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    AuthService(db).verify_token(datos.access_token)
    usuarios = (
        db.query(
            Usuarios.id_usuario,
            Usuarios.nombre,
            Usuarios.correo,
            Usuarios.activo,
            Rol.nombre.label("rol"),
        )
        .join(Rol, Usuarios.id_rol == Rol.id_rol)
        .all()
    )
    return [
        {
            "id_usuario": u.id_usuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "activo": u.activo,
            "rol": u.rol,
        }
        for u in usuarios
    ]


@router.post("/asignaturas/lista")
def listar_asignaturas(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    AuthService(db).verify_token(datos.access_token)
    return db.query(Asignaturas).all()


@router.post("/clases/lista")
def listar_clases(datos: TokenVerifySchema, db: Session = Depends(get_db)):
    AuthService(db).verify_token(datos.access_token)
    clases = (
        db.query(
            Clases.id_clase,
            Clases.periodo_academico,
            Clases.grupo,
            Clases.cupo_maximo,
            Asignaturas.nombre_materia,
            Usuarios.nombre.label("docente"),
        )
        .join(Asignaturas, Clases.id_asignatura == Asignaturas.id_asignatura)
        .join(Usuarios, Clases.id_docente == Usuarios.id_usuario)
        .all()
    )
    return [
        {
            "id_clase": c.id_clase,
            "nombre_materia": c.nombre_materia,
            "docente": c.docente,
            "periodo_academico": c.periodo_academico,
            "grupo": c.grupo,
            "cupo_maximo": c.cupo_maximo,
        }
        for c in clases
    ]
