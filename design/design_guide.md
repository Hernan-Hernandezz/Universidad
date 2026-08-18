# Guía de Diseño Completa: Plataforma Estudiantil Inteligente

Esta guía compila los fundamentos teóricos, principios de UI/UX, requisitos de diseño y especificaciones visuales indispensables para la construcción de los mockups y prototipos de la plataforma.

---

## 1. Fundamentos Teóricos de UI/UX

El diseño de interfaces no se limita a la estética visual; representa una solución funcional estructurada a problemas concretos de interacción y usabilidad.

### Definiciones Clave de Componentes Visuales

- **Wireframe:** Representación esquemática y estructural básica de la interfaz. Su objetivo es definir la distribución de los componentes y la arquitectura de la información en la pantalla, prescindiendo completamente del uso de colores, imágenes o tipografías finales.
- **Mockup:** Diseño visual detallado de alta fidelidad. Integra la identidad gráfica definida para el proyecto mediante el uso de paletas de colores, tipografías específicas, botones estilizados, iconos e imágenes. Es una simulación estática pero realista del sistema final.
- **Prototipo:** Evolución interactiva del mockup. Consiste en la interconexión de las diferentes pantallas diseñadas con el fin de simular la navegación real, los flujos de retorno, los clics en los elementos interactivos y la experiencia de usuario general antes de la etapa de desarrollo de software.

### Principios Fundamentales de Diseño UI

- **Jerarquía Visual:** Organización de los elementos de tal manera que lo más importante capte la atención del usuario en primer lugar. Se logra mediante variaciones de tamaño, peso tipográfico y contraste de color.
- **Espaciado (White Space):** Uso estratégico del espacio libre para evitar la saturación de las pantallas. Facilita la legibilidad y permite que la interfaz respire.
- **Consistencia:** Mantenimiento riguroso de patrones visuales y de comportamiento en todo el sistema. Los botones, la iconografía y las reglas de color deben comportarse de la misma manera en todas las pantallas.
- **Contraste:** Garantía de que los elementos interactivos, textos y estados críticos sean perfectamente distinguibles por el usuario, promoviendo la claridad y la accesibilidad.
- **Simplicidad:** Reducción de elementos innecesarios. Menos elementos en pantalla se traducen directamente en una carga cognitiva menor y una mejor experiencia de usuario.

---

## 2. Sistema de Diseño (UI Specifications)

Para garantizar la consistencia en todas las vistas de la aplicación web y móvil, se establece el siguiente sistema de diseño cerrado:

### Tipografía

- **Tipografía Principal:** **Roboto (Sans-Serif)**. Seleccionada específicamente por su alta legibilidad en pantallas digitales, suavidad en interfaces densas y adaptabilidad en componentes web y móviles.
- **Tipografía Técnica/Numérica:** **Roboto Mono (Monospaced)**. Destinada exclusivamente al despliegue de datos numéricos, tablas de calificaciones, porcentajes y la interfaz interactiva de simulación de notas.

### Paleta de Colores (Enfoque Monocromático y de Alerta)

- `#004959` (Color Oscuro / Serio): Utilizado para fondos principales de encabezados, barras de navegación laterales (sidebars) y texto de alta prioridad.
- `#368FA2` (Color Medio / Identidad): Utilizado para componentes interactivos principales, botones de acción primaria, enlaces activos y elementos destacados de la marca.
- `#ACF2FF` (Color Claro / Contraste): Utilizado para fondos de tarjetas (cards), estados seleccionados, contenedores secundarios y para generar contraste limpio con el texto oscuro.
- `#AE443A` (Color de Alerta / Crítico): Utilizado estrictamente para estados de error de acceso, alertas del sistema de alta prioridad, tareas vencidas y notificaciones críticas de bienestar.

### Iconografía

- **Librería Base:** [Phosphor Icons](https://phosphoricons.com/). Todos los iconos del sistema deben extraerse de esta librería para mantener un grosor de línea, estilo y geometría consistente en toda la plataforma.

---

## 3. Arquitectura e Información de los Módulos del Sistema

Cada una de las vistas diseñadas debe estructurarse respondiendo formalmente a cuatro preguntas de control de diseño:

1. _¿Qué acción hará primero el usuario en esta pantalla?_
2. _¿La pantalla está saturada de componentes?_
3. _¿Los botones y llamadas a la acción son claros?_
4. _¿La navegación es intuitiva y rápida?_

### 1. Módulo de Autenticación

- **Pantallas requeridas:**
  - _Login:_ Formulario limpio con campos de usuario/correo, contraseña, botón de acción primaria con color `#368FA2` y enlaces secundarios.
  - _Recuperar Contraseña:_ Flujo simplificado solicitando el correo electrónico para el envío de instrucciones de restablecimiento.
  - _Verificación de Correo:_ Vista de confirmación con estados visuales claros (ej. códigos de verificación o mensajes de éxito).
  - _Pantalla de Carga (Splash Screen):_ Estado de transición visual con un indicador de carga limpio e isotipo de la institución.
  - _Error de Acceso:_ Destaque visual utilizando el color de alerta `#AE443A` ante credenciales inválidas o fallas de conexión.

### 2. Dashboard Principal

Debe actuar como un centro de control unificado y centralizado para el estudiante, mostrando de forma resumida e inteligente los siguientes bloques de datos:

- **Resumen Académico:** Estado general del periodo actual (promedio ponderado o progreso).
- **Próximas Clases:** Horario del día actual con indicación explícita del salón y la hora.
- **Tareas Pendientes:** Listado priorizado cronológicamente con fechas de entrega.
- **Alertas Importantes:** Notificaciones críticas institucionales o académicas destacadas.
- **Estado Emocional Semanal:** Indicador visual simplificado derivado del módulo de bienestar.
- **Accesos Rápidos:** Botones directos a las funcionalidades más utilizadas del sistema (ej. solicitar tutoría, simular notas).

### 3. Gestión de Horarios

- **Funcionalidades Visuales:**
  - Vista de calendario/horario semanal clara y responsiva.
  - Detección visual de conflictos de horarios (solapamientos de clases).
  - Actualizaciones en tiempo real ante cambios de asignaturas o profesores.
  - Visualización interactiva y destacada de los salones de clase para evitar la desorientación física del alumno.

### 4. Gestión Académica

- **Funcionalidades Visuales:**
  - Desglose visual detallado de las materias inscritas por el estudiante.
  - Visualización clara de los porcentajes de evaluación asignados a cada corte académico.
  - **Simulador de Rendimiento:** Interfaz interactiva que permite al usuario registrar notas simuladas para proyectar el promedio requerido para aprobar una asignatura.
  - Gráficos limpios o indicadores de análisis de rendimiento histórico.

### 5. Bienestar Estudiantil

- **Funcionalidades Visuales:**
  - _Test Emocional:_ Interfaz amigable e introspectiva para responder cuestionarios de seguimiento psicológico.
  - _Solicitud de Apoyo:_ Canal ágil y confidencial para requerir asistencia profesional.
  - _Agenda Psicológica:_ Calendario de citas integrado con disponibilidad de profesionales en tiempo real.
  - _Recomendaciones Automatizadas:_ Mensajes y consejos sugeridos de forma inteligente basados en el estado del estudiante.

### 6. Comunicación

- **Funcionalidades Visuales:**
  - _Chat con Docentes:_ Bandeja de mensajería directa y organizada por materias.
  - _Mensajes Automáticos / Notificaciones:_ Alertas del sistema sobre eventos o cambios.
  - _Anuncios Institucionales:_ Tablón digital de noticias de la institución educativa.

---

## 4. Retos Técnicos de UX/UI a Resolver

- **Evitar la saturación visual:** Balancear la densidad de los datos utilizando amplios espacios en blanco y colapsando información secundaria.
- **Navegación Rápida:** Diseñar estructuras de menús (sidebars en web, bottom bars en móvil) que permitan acceder a cualquier módulo en menos de 3 clics.
- **Interfaz Responsive:** Asegurar la adaptabilidad fluida de todos los componentes de la aplicación web a pantallas móviles sin perder usabilidad ni legibilidad tipográfica.
