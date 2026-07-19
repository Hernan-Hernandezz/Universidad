
-- busca las asignaturas y su horario de un estudiante

SELECT
  u.nombre            AS estudiante,
  a.nombre_materia    AS materia,
  d.dia,
  h.hora_inicio,
  h.hora_fin,
  au.codigo           AS aula
FROM "Matriculas"     m
JOIN "Usuarios"       u  ON m.id_estudiante = u.id_usuario
JOIN "Clases"         c  ON m.id_clase      = c.id_clase
JOIN "Asignaturas"    a  ON c.id_asignatura = a.id_asignatura
JOIN "Clases_Horario" h  ON h.id_clase      = c.id_clase
JOIN "Aulas"          au ON h.id_aula       = au.id_aula
JOIN "Dia_Semana"     d  ON h.id_dia_semana = d.id_dia_semana
WHERE m.id_estudiante = 1 ORDER BY d.id_dia_semana  ASC, h.hora_inicio ASC;

--busca las asignaturas y su horario de todos los estudiantes

SELECT
  u.nombre            AS estudiante,
  a.nombre_materia    AS materia,
  h.id_dia_semana,
  h.id_clase,
  h.hora_inicio,
  h.hora_fin,
  au.codigo           AS aula
FROM "Matriculas"     m
JOIN "Usuarios"       u  ON m.id_estudiante = u.id_usuario
JOIN "Clases"         c  ON m.id_clase      = c.id_clase
JOIN "Asignaturas"    a  ON c.id_asignatura = a.id_asignatura
JOIN "Clases_Horario" h  ON h.id_clase      = c.id_clase
JOIN "Aulas"          au ON h.id_aula       = au.id_aula
WHERE u.id_rol = 1;

-- busca las notas por asignaturas de un estudiante

SELECT
  u.nombre,
  a.nombre_materia,
  m.nota_final
FROM "Matriculas" m
JOIN "Usuarios"    u ON m.id_estudiante  = u.id_usuario
JOIN "Clases"      c ON m.id_clase       = c.id_clase
JOIN "Asignaturas" a ON c.id_asignatura  = a.id_asignatura
WHERE u.id_usuario = 2;


-- buscar tareas pendiente por estudiante

SELECT
  u.nombre,
  a.nombre_materia AS asignatura,
  t.titulo_tarea,
  t.fecha_entrega,
  te.id_estado_tarea
  FROM "Tareas_Estudiante" te
  JOIN "Matriculas"     m ON te.id_matricula  = m.id_matricula
  JOIN "Clases"         c ON m.id_clase       = c.id_clase
  JOIN "Tareas"         t ON te.id_tarea      = t.id_tarea
  JOIN "Asignaturas"    a ON c.id_asignatura  = a.id_asignatura
  JOIN "Usuarios"       u ON m.id_estudiante  = u.id_usuario
  WHERE u.id_usuario = 2
  ;

SELECT
  u.nombre  AS estudiante,
  a.nombre_materia  AS materia,
  t.titulo_tarea,
  t.fecha_entrega,
  et.nombre_estado  AS estado
FROM "Tareas_Estudiante" te
JOIN "Matriculas"    m  ON te.id_matricula    = m.id_matricula
JOIN "Usuarios"      u  ON m.id_estudiante    = u.id_usuario
JOIN "Tareas"        t  ON te.id_tarea        = t.id_tarea
JOIN "Clases"        c  ON t.id_clase         = c.id_clase
JOIN "Asignaturas"   a  ON c.id_asignatura    = a.id_asignatura
JOIN "Estado_Tareas" et ON te.id_estado_tarea = et.id_estado_tarea
ORDER BY u.nombre ASC,t.fecha_entrega ASC;



