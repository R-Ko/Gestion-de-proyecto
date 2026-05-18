# Arquitectura y Lógica del Sistema - Gestión de Proyectos

## 📋 Descripción General

Esta es una aplicación web tipo **ERP/Project Management** construida con **Flask** que replica el diseño visual de **Odoo**. El sistema permite gestionar proyectos, tareas, usuarios y sus permisos dentro de una estructura jerárquica.

**Objetivo**: Sistema de gestión de proyectos y tareas con autenticación de usuarios, control de acceso y seguimiento de cambios.

---

## 🏗️ Stack Tecnológico

### Backend
- **Framework**: Flask (Python)
- **Base de datos**: SQLite (desarrollo) o PostgreSQL (producción)
- **Seguridad**: Werkzeug (hashing de contraseñas)
- **Autenticación**: Sessions (Flask)

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Diseño moderno con gradientes y animaciones
- **Tema**: Estilo Odoo (paleta oscura: púrpura, azul, cyan)
- **Responsive**: Mobile-first con grid CSS moderno

---

## 🗄️ Estructura de Base de Datos

### Tablas Principales

#### `users`
```
- id (INT PK)
- email (TEXT, UNIQUE)
- password (TEXT, hashed)
```
**Usuarios del sistema con autenticación segura.**

#### `projects`
```
- id (INT PK)
- name (TEXT)
- owner_email (TEXT)
- assigned_emails (TEXT, CSV de correos)
- tasks_count (INT)
- tickets_count (INT)
```
**Proyectos con propietario y usuarios asignados.**

#### `tasks`
```
- id (INT PK)
- project_id (INT FK)
- title (TEXT)
- description (TEXT)
- assigned_email (TEXT)
- stage (TEXT) [backlog, pending, inprogress, qa, validation, deployed]
- task_type (TEXT) [Codificación, Análisis, Documentación, Despliegue]
- deadline (TEXT)
- milestone (TEXT)
- sprint (TEXT)
- category (TEXT)
- status (TEXT)
- ticket_number (TEXT)
- created_at (TEXT)
```
**Tareas individuales dentro de proyectos con ciclo de vida completo.**

#### `task_changes`
```
- id (INT PK)
- task_id (INT FK)
- author (TEXT)
- note (TEXT)
- changed_at (TEXT)
```
**Historial/Auditoría de cambios en tareas.**

#### `user_allowed_projects`
```
- user_id (INT FK)
- project_id (INT FK)
- PRIMARY KEY (user_id, project_id)
```
**Control de acceso: qué usuarios pueden ver qué proyectos.**

---

## 🔐 Flujo de Autenticación

```
┌─────────────────────────────────────────────────────┐
│ USUARIO NO AUTENTICADO                              │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────▼──────────┐
         │ /login GET       │
         │ (login.html)     │
         └───────┬──────────┘
                 │
         ┌───────▼──────────────────┐
         │ Usuario ingresa datos    │
         └───────┬──────────────────┘
                 │
         ┌───────▼──────────────────────────────────┐
         │ POST /login (validar email + password)  │
         └───────┬───────────────────────────────────┘
                 │
         ┌───────▼──────────────────────┐
         │ ✓ Contraseña válida          │
         │ → Crear session              │
         │ → Redirigir a /dashboard     │
         └──────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────┐
│ USUARIO AUTENTICADO                               │
│ session.user = email del usuario                  │
└───────────────────────────────────────────────────┘
```

**Rutas públicas**:
- `/login` - Formulario de login
- `/reset` - Restablecer contraseña / crear cuenta
- `/superuser` - Login como administrador

**Rutas protegidas** (requieren `session.user`):
- `/dashboard` - Página principal
- `/app/*` - Módulos y apps
- `/project/*` - Gestión de proyectos
- `/logout` - Cerrar sesión

---

## 📱 Módulos/Apps Disponibles

El sistema implementa un menú de módulos similar a Odoo:

```html
┌─────────────────────────────────────────────┐
│ Dashboard  Projects  Tasks  Users  Settings │
└─────────────────────────────────────────────┘
     │         │         │       │      │
     ├─ Proyectos
     ├─ Tareas
     ├─ Usuarios
     ├─ Configuración
     └─ etc...
```

### Cada módulo tiene:
- **Vista de lista**: `/app/{modulo}` (ej: `/app/project`)
- **Vista de detalle**: `/{modulo}/{id}` (ej: `/project/1`)
- **Crear**: `/create/{modulo}` (ej: `/create/project`)

---

## 🎯 Flujo de Funcionalidades Principales

### 1. Gestión de Proyectos

```
LISTAR PROYECTOS
├─ GET /app/project
├─ Filtros disponibles:
│  ├─ Todos (all)
│  ├─ Asignados (assigned)
│  ├─ Hitos (hitos)
│  └─ Sprint (sprint)
├─ Mostrar grid con tarjetas
└─ Cada tarjeta:
   ├─ Nombre del proyecto
   ├─ Descripción
   ├─ Contador de tasks
   ├─ Contador de tickets
   └─ Link a detalle
```

### 2. Ver Detalle de Proyecto

```
GET /project/{id}
├─ Información del proyecto
│  ├─ Nombre
│  ├─ Propietario
│  ├─ Usuarios asignados
│  └─ Estadísticas
├─ Lista de TAREAS
│  ├─ Tabla con columns: ID, Título, Asignado, Stage, Deadline
│  ├─ Filtros por stage
│  └─ Acciones: Editar, Eliminar, Cambiar estado
└─ Opciones: Editar proyecto, Eliminar proyecto
```

### 3. Ciclo de Vida de Tareas

Una tarea transita por estos **stages**:

```
BACKLOG → PENDIENTE → EN PROGRESO → QA → VALIDACIÓN → DESPLEGADA
   ↑                                            ↓
   └────────────────── (rechazada) ──────────┘
```

Cada transición de **stage** genera un **cambio registrado** en `task_changes`.

### 4. Gestión de Cambios

Cada vez que una tarea cambia:
- Se registra el **autor** del cambio
- Se guarda la **nota** (qué cambió)
- Se almacena el **timestamp**

Visible en: Vista de detalle de tarea → Sección "Historial"

---

## 🎨 Diseño Visual / Paleta de Colores

### Tema Oscuro Odoo

```css
Color          | Uso
─────────────────────────────────────────────
#0d1230        | Fondo principal (--surface)
#10184d        | Fondo secundario (--surface-strong)
#7c3aed        | Primario: botones, acentos (--accent: púrpura)
#38bdf8        | Secundario: estados, links (--accent-alt: cyan/azul)
#edf2ff        | Texto principal (--text: blanco roto)
#cbd5e1        | Texto secundario (--text-muted: gris claro)
```

### Componentes Comunes

1. **Topbar**: Gradiente oscuro, usuario, logout
2. **Tarjetas (proj-card)**: Fondo oscuro, border sutil, hover con elevación
3. **Botones**: Gradientes, sombras, transiciones suaves
4. **Tablas**: Filas alternas, hover, responsive
5. **Filtros/Busca**: Diseño en píldoras (pills)
6. **Badges**: Estados en colores de cyan o púrpura

---

## 📄 Estructura de Templates

```
templates/
├── login.html              # Página de login (público)
├── superuser.html          # Login especial (público)
├── reset.html              # Reset de contraseña / crear cuenta (público)
├── app_page.html           # Template base para apps
├── apps.html               # Grid de módulos disponibles
├── dashboard.html          # Dashboard principal
├── project_list.html       # Listado de proyectos con filtros
├── project_detail.html     # Detalle de proyecto + tareas
├── project_create.html     # Formulario crear proyecto
├── task_create.html        # Formulario crear tarea
├── task_detail.html        # Detalle de tarea + historial
├── users.html              # Listado de usuarios
├── user_edit.html          # Editar usuario
└── wizard_change_password.xml  # Cambio de contraseña
```

---

## 🔄 Estados y Ciclos de Tareas

### Stages disponibles

| Stage | Label | Color | Significado |
|-------|-------|-------|-------------|
| `backlog` | Backlog | Gris | No iniciada, en cola |
| `pending` | Pendientes/Detenidas | Rojo | Esperando acción |
| `inprogress` | En progreso | Amarillo | Siendo trabajada |
| `qa` | QA | Azul | En control de calidad |
| `validation` | Validación | Púrpura | Esperando aprobación |
| `deployed` | Desplegada | Verde | Completada |

### Mapeo automático Stage → Status

```python
STAGE_STATUS_MAP = {
    'backlog': 'Pendiente',
    'pending': 'Pendiente',
    'inprogress': 'En progreso',
    'qa': 'QA',
    'validation': 'Validación',
    'deployed': 'Desplegada',
}
```

---

## 🚀 Rutas Principales de la Aplicación

### Públicas (sin autenticación)
```
GET    /login                  → Mostrar formulario login
POST   /login                  → Procesar login
GET    /reset                  → Página reset password / crear cuenta
GET    /superuser              → Login como admin
```

### Privadas (requieren sesión)
```
GET    /dashboard              → Página principal
GET    /logout                 → Cerrar sesión

GET    /app/project            → Listar proyectos
GET    /app/project?filter=... → Filtrar proyectos
GET    /project/{id}           → Ver detalle proyecto
POST   /project/{id}/update    → Actualizar proyecto
POST   /project/{id}/delete    → Eliminar proyecto

GET    /create/project         → Formulario crear proyecto
POST   /create/project         → Guardar nuevo proyecto

GET    /task/{id}              → Ver detalle tarea
POST   /task/{id}/update       → Actualizar tarea
POST   /task/{id}/delete       → Eliminar tarea
POST   /task/{id}/stage        → Cambiar stage de tarea

GET    /create/task            → Formulario crear tarea
POST   /create/task            → Guardar nueva tarea

GET    /app/users              → Listar usuarios
GET    /user/{id}              → Ver usuario
POST   /user/{id}/edit         → Editar usuario
POST   /user/change-password   → Cambiar contraseña
```

---

## 🔐 Control de Acceso

### Niveles de permisos:

1. **Usuario normal**: 
   - Ve solo sus proyectos asignados
   - Puede editar tareas asignadas
   - No puede modificar permisos

2. **Propietario de proyecto**:
   - Ve y edita todas las tareas del proyecto
   - Puede asignar usuarios
   - Puede cambiar settings

3. **Admin/Superuser**:
   - Acceso total a todo
   - Gestiona usuarios
   - Gestiona permisos

### Validación:
```python
if session.user not in allowed_users_for_project:
    return redirect('/apps')  # Redirigir si no tiene acceso
```

---

## 📊 Datos de Ejemplo

### Usuarios de Demo
```
admin@example.com        / admin
demo@example.com         / demo
leandro@example.com      / demo
other@example.com        / demo
ce@example.com           / demo
```

### Proyectos de Demo
1. **Pyxel Odin Bayon** - 9 tasks, 0 tickets (Propietario: admin)
2. **Pyxel Odin JKY** - 2 tasks, 0 tickets (Propietario: demo)
3. **Level 1** - 1 task, 0 tickets (Propietario: other)
4. **Comercio Electrónico** - 331 tasks, 0 tickets (Propietario: ce)

### Tareas de Demo
- Cada tarea tiene: título, descripción, asignado, stage, deadline, milestone, sprint, categoría, número de ticket
- Ejemplos: migración de módulos, ajustes, despliegue, etc.

---

## 🎯 Mejoras de UX/Frontend Sugeridas

### Para V0 - Consideraciones de diseño:

1. **Responsive mejorado**: Asegurar que grid/tablas se adapten bien en móvil
2. **Animaciones**: Transiciones al cambiar stage, loading states
3. **Dark mode completamente consistente**: Aplicar tema en todos los inputs y selects
4. **Validación en tiempo real**: Feedback inmediato en formularios
5. **Indicadores visuales**: Estados de tareas con iconos + colores
6. **Tooltips/Help**: Explicar campos complejos
7. **Paginación inteligente**: Para proyectos con muchas tareas
8. **Búsqueda avanzada**: Filtros más complejos en proyectos
9. **Drag & drop**: Mover tareas entre stages visualmente
10. **Notificaciones**: Toast alerts para acciones completadas

---

## 🔧 Flujo de Desarrollo Frontend

### Stack Frontend recomendado para mejorar:
- **Tailwind CSS** o mantener CSS actual con mejor organización
- **Alpine.js** o **htmx** para interactividad sin framework pesado
- **Chart.js** para gráficos de proyectos
- **Select2** o similar para dropdowns mejorados
- **Sortable.js** para drag & drop

---

## 📝 Notas de Implementación

- El sistema es **multi-tenant**: Diferentes usuarios ven diferentes proyectos
- **Auditoría completa**: Todo cambio se registra en `task_changes`
- **Escalable**: Soporta PostgreSQL para producción
- **Modular**: Fácil agregar nuevos módulos/apps
- **Seguridad**: Contraseñas hasheadas con Werkzeug
