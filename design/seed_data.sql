-- =============================================
-- DATOS DE PRUEBA - Plataforma Estudiantil
-- Ejecutar en orden, respeta llaves foráneas
-- =============================================

-- 1. ROLES
INSERT INTO "Rol" (nombre) VALUES
  ('estudiante'),
  ('docente'),
  ('admin');

-- 2. USUARIOS (3 estudiantes, 3 docentes, 1 admin)
INSERT INTO "Usuarios" (nombre, correo, contrasena_hash, id_rol) VALUES
  ('Carlos Pérez',    'carlos@edu.com',   'carlos123',   1),
  ('María López',     'maria@edu.com',    'maria123',    1),
  ('Juan Torres',     'juan@edu.com',     'juan123',     1),
  ('Luis Ramírez',    'luis@edu.com',     'luis123',     1),
  ('Ana Gómez',       'ana@edu.com',      'ana123',      1),
  ('Andrea Ruiz',     'andrea@edu.com',   'andrea123',   2),
  ('Roberto Mora',    'roberto@edu.com',  'roberto123',  2),
  ('Patricia Silva',  'patricia@edu.com', 'patricia123', 2),
  ('Admin Sistema',   'admin@edu.com',    'admin123',    3);

UPDATE "Usuarios" SET contrasena_hash='admin123' WHERE id_usuario=9;


-- 3. ASIGNATURAS
INSERT INTO "Asignaturas" (codigo, nombre_materia, creditos) VALUES
  ('PRO-101', 'Programación I',     3),
  ('MAT-101', 'Matemáticas I',      3),
  ('FIS-101', 'Física I',           3),
  ('ING-101', 'Inglés I',           2),
  ('BDD-101', 'Bases de Datos I',   3);

-- 4. AULAS
INSERT INTO "Aulas" (codigo, numero_bloque, numero_salon, capacidad, tipo) VALUES
  ('A-101', 'A', '101', 30, 'salon'),
  ('A-102', 'A', '102', 30, 'salon'),
  ('B-201', 'B', '201', 25, 'salon'),
  ('B-LAB', 'B', '301', 20, 'laboratorio'),
  ('C-AUD', 'C', '001', 80, 'auditorio');

-- 5. CLASES (cada asignatura con un docente)
-- Andrea(6)=PRO,FIS,BDD  Roberto(7)=MAT  Patricia(8)=ING
INSERT INTO "Clases" (id_asignatura, id_docente, periodo_academico, grupo, cupo_maximo) VALUES
  (1, 6, '2026-1', '01', 35),
  (2, 7, '2026-1', '01', 35),
  (3, 6, '2026-1', '01', 35),
  (4, 8, '2026-1', '01', 35),
  (5, 6, '2026-1', '01', 35);

-- 6. ESTADO MATRÍCULA
INSERT INTO "Estado_Matricula" (estado) VALUES
  ('Activa'),
  ('Cancelada'),
  ('Finalizada');

-- 7. DIA SEMANA
INSERT INTO "Dia_Semana" (dia) VALUES
  ('Lunes'),
  ('Martes'),
  ('Miércoles'),
  ('Jueves'),
  ('Viernes');

-- 8. MATRÍCULAS
-- Carlos(1): PRO, MAT, BDD
-- María(2):  PRO, FIS, ING
-- Juan(3):   MAT, FIS, BDD
-- Luis(4):   PRO, ING, MAT
-- Ana(5):    FIS, BDD, ING
INSERT INTO "Matriculas" (id_estudiante, id_clase, id_estado_matricula) VALUES
  (1, 1, 1), (1, 2, 1), (1, 5, 1),
  (2, 1, 1), (2, 3, 1), (2, 4, 1),
  (3, 2, 1), (3, 3, 1), (3, 5, 1),
  (4, 1, 1), (4, 4, 1), (4, 2, 1),
  (5, 3, 1), (5, 5, 1), (5, 4, 1);

-- 9. HORARIOS
-- Clase 1 PRO: Lunes y Miércoles 8-10am en A-101
-- Clase 2 MAT: Martes y Jueves 10-12pm en A-102
-- Clase 3 FIS: Lunes y Viernes 2-4pm en B-LAB
-- Clase 4 ING: Miércoles 8-10am en B-201
-- Clase 5 BDD: Martes y Jueves 2-4pm en A-101
INSERT INTO "Clases_Horario" (id_clase, id_aula, id_dia_semana, hora_inicio, hora_fin) VALUES
  (1, 1, 1, '08:00', '10:00'),
  (1, 1, 3, '08:00', '10:00'),
  (2, 2, 2, '10:00', '12:00'),
  (2, 2, 4, '10:00', '12:00'),
  (3, 4, 1, '14:00', '16:00'),
  (3, 4, 5, '14:00', '16:00'),
  (4, 3, 3, '08:00', '10:00'),
  (5, 1, 2, '14:00', '16:00'),
  (5, 1, 4, '14:00', '16:00');

-- 10. ESTADO TAREAS
INSERT INTO "Estado_Tareas" (nombre_estado) VALUES
  ('Pendiente'),
  ('Entregado'),
  ('Calificado'),
  ('Simulado');

-- 11. TAREAS (2-3 por clase, distintos cortes)
INSERT INTO "Tareas" (id_clase, creado_por, titulo_tarea, descripcion, fecha_entrega, porcentaje_dentro_corte, corte) VALUES
  -- Programación (clase 1, docente Andrea=6)
  (1, 6, 'Taller de variables',     'Ejercicios de variables y tipos de datos en Python', '2026-07-15 23:59', 20, 1),
  (1, 6, 'Taller de ciclos',        'Ejercicios con for y while',                         '2026-08-01 23:59', 30, 1),
  (1, 6, 'Proyecto corte 1',        'Mini aplicación en Python con funciones',             '2026-08-20 23:59', 50, 1),

  -- Matemáticas (clase 2, docente Roberto=7)
  (2, 7, 'Taller de límites',       'Ejercicios de límites y continuidad',                '2026-07-20 23:59', 30, 1),
  (2, 7, 'Parcial de integrales',   'Evaluación de integrales definidas',                 '2026-08-10 23:59', 40, 1),
  (2, 7, 'Trabajo grupal',          'Análisis de funciones trigonométricas',              '2026-08-25 23:59', 30, 1),

  -- Física (clase 3, docente Andrea=6)
  (3, 6, 'Informe laboratorio',     'Informe sobre movimiento rectilíneo uniforme',       '2026-07-18 23:59', 25, 1),
  (3, 6, 'Taller de vectores',      'Ejercicios de suma y resta de vectores',             '2026-08-05 23:59', 25, 1),
  (3, 6, 'Parcial de física',       'Evaluación de cinemática y dinámica',                '2026-08-22 23:59', 50, 1),

  -- Inglés (clase 4, docente Patricia=8)
  (4, 8, 'Reading comprehension',   'Lectura y preguntas sobre texto en inglés',          '2026-07-25 23:59', 30, 1),
  (4, 8, 'Speaking parcial',        'Conversación oral sobre rutinas diarias',            '2026-08-15 23:59', 40, 1),

  -- Bases de Datos (clase 5, docente Andrea=6)
  (5, 6, 'Taller de SQL',           'Consultas SELECT, JOIN y WHERE',                     '2026-07-22 23:59', 25, 1),
  (5, 6, 'Diseño ER',               'Diseño de diagrama entidad-relación',                '2026-08-08 23:59', 25, 1),
  (5, 6, 'Proyecto BD',             'Implementación de base de datos completa',           '2026-08-28 23:59', 50, 1);

-- 12. ASIGNAR TAREAS A ESTUDIANTES AUTOMÁTICAMENTE
INSERT INTO "Tareas_Estudiante" (id_matricula, id_tarea, id_estado_tarea, nota, es_simulada)
SELECT
  m.id_matricula,
  t.id_tarea,
  1,      -- Pendiente
  NULL,
  false
FROM "Tareas" t
JOIN "Matriculas" m ON m.id_clase = t.id_clase
WHERE m.id_estado_matricula = 1
ON CONFLICT DO NOTHING;

-- 13. AGREGAR ALGUNAS NOTAS A TAREAS YA CALIFICADAS
-- Carlos - Taller variables (id_tarea=1, id_matricula=1)
UPDATE "Tareas_Estudiante" SET nota = 4.2, id_estado_tarea = 3
WHERE id_matricula = 1 AND id_tarea = 1;

-- María - Taller variables (id_tarea=1, id_matricula=4)
UPDATE "Tareas_Estudiante" SET nota = 3.8, id_estado_tarea = 3
WHERE id_matricula = 4 AND id_tarea = 1;

-- Juan - Taller de límites (id_tarea=4, id_matricula=6)
UPDATE "Tareas_Estudiante" SET nota = 4.5, id_estado_tarea = 3
WHERE id_matricula = 6 AND id_tarea = 4;

-- Luis - Taller de límites (id_tarea=4, id_matricula=11)
UPDATE "Tareas_Estudiante" SET nota = 3.5, id_estado_tarea = 3
WHERE id_matricula = 11 AND id_tarea = 4;

-- Ana - Informe laboratorio (id_tarea=7, id_matricula=13)
UPDATE "Tareas_Estudiante" SET nota = 4.8, id_estado_tarea = 3
WHERE id_matricula = 13 AND id_tarea = 7;

-- Algunas tareas entregadas pero sin calificar
UPDATE "Tareas_Estudiante" SET id_estado_tarea = 2, entregado_en = now()
WHERE id_matricula = 1 AND id_tarea = 2;

UPDATE "Tareas_Estudiante" SET id_estado_tarea = 2, entregado_en = now()
WHERE id_matricula = 4 AND id_tarea = 2;
