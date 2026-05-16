from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    # create a default user and sample users
    try:
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                    ('admin@example.com', generate_password_hash('admin')))
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                    ('demo@example.com', generate_password_hash('demo')))
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                    ('leandro@example.com', generate_password_hash('demo')))
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                    ('other@example.com', generate_password_hash('demo')))
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                    ('ce@example.com', generate_password_hash('demo')))
    except Exception:
        pass
    conn.commit()
    conn.close()

    # create a simple projects table for demo
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        owner_email TEXT,
        assigned_emails TEXT,
        tasks_count INTEGER DEFAULT 0,
        tickets_count INTEGER DEFAULT 0
    )
    ''')
    # seed some demo projects if empty
    cur.execute('SELECT COUNT(*) FROM projects')
    if cur.fetchone()[0] == 0:
        demo = [
            ('Pyxel Odin Bayon', 'admin@example.com', 'admin@example.com,demo@example.com,leandro@example.com', 9, 0),
            ('Pyxel Odin JKY', 'demo@example.com', 'demo@example.com', 2, 0),
            ('Level 1', 'other@example.com', 'other@example.com,admin@example.com', 1, 0),
            ('Comercio Electrónico', 'ce@example.com', 'ce@example.com', 331, 0),
        ]
        cur.executemany('INSERT INTO projects (name, owner_email, assigned_emails, tasks_count, tickets_count) VALUES (?,?,?,?,?)', demo)

    cur.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        assigned_email TEXT,
        stage TEXT,
        task_type TEXT,
        deadline TEXT,
        milestone TEXT,
        sprint TEXT,
        category TEXT,
        status TEXT,
        ticket_number TEXT,
        created_at TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS task_changes (
        id INTEGER PRIMARY KEY,
        task_id INTEGER NOT NULL,
        author TEXT,
        note TEXT,
        changed_at TEXT
    )
    ''')

    cur.execute('SELECT COUNT(*) FROM tasks')
    if cur.fetchone()[0] == 0:
        demo_tasks = [
            (1, 'PyxelSolutions Odin (Localización Cubana) | Ajustes | No visualizar el módulo de Inventario si se configura que el usuario no tiene acceso al mismo', 'Ajuste de permisos en el módulo de inventario para usuarios sin acceso.', 'leandro@example.com', 'backlog', 'Funcionalidad', '2026-01-31', 'Certificación del producto', 'Sprint 1', 'Nacional', 'Pendiente', '16985', '2025-12-18'),
            (1, 'Revisión de documentación realiza 9.130', 'Revisión de la documentación del plan inicial con el equipo de proyecto.', 'demo@example.com', 'pending', 'Documentación', '2026-02-15', 'Plan Inicial del Proyecto', 'Sprint 1', 'Nacional', 'Pendiente', '9130', '2025-12-20'),
            (1, 'PyxelSolutions Odin (Localización Cubana) | Ajustes | Establecer un mecanismo de CAPTCHA en la funcionalidad de restablecimiento de contraseña', 'Implementar CAPTCHA en la pantalla de restablecimiento para evitar ataques de fuerza bruta.', 'admin@example.com', 'inprogress', 'Funcionalidad', '2025-12-18', 'Certificación del producto', 'Sprint 2', 'Nacional', 'En progreso', '16997', '2025-11-30'),
            (1, 'PyxelSolutions Odin (Localización Cubana) | Facturación | Migrar de Odoo 14 el módulo Bloqueo de Período fiscal', 'Adaptar el módulo de bloqueo de período fiscal para la nueva versión y cierre automático.', 'leandro@example.com', 'qa', 'Codificación', '2025-11-07', 'Cobros', 'Sprint 2', 'Nacional', 'QA', '16522', '2025-10-12'),
            (1, 'PyxelSolutions Odin (Localización Cubana) | Nómina | Migración del módulo pyxel_hr_payroll_submayor (Odoo 14 → Odoo 17)', 'Migración de nómina y salarios a Odoo 17 con validación de submayor fiscal.', 'demo@example.com', 'validation', 'Codificación', '2025-11-19', 'Nómina', 'Sprint 3', 'Nacional', 'Validación', '16687', '2025-09-15'),
            (1, 'PyxelSolutions Odin (Localización Cubana) | Despliegue | Verificar instalación en servidor de producción', 'Comprobación final del despliegue en el servidor de producción.', 'admin@example.com', 'deployed', 'Despliegue', '2026-04-01', 'Go-live', 'Sprint 4', 'Nacional', 'Desplegada', '17001', '2026-03-25'),
            (1, 'PyxelSolutions Odin (Localización Cubana) | Despliegue | Validar migración de datos en staging', 'Pruebas de migración de datos en el entorno de staging antes del release.', 'leandro@example.com', 'deployed', 'Despliegue', '2026-03-12', 'Go-live', 'Sprint 4', 'Nacional', 'Desplegada', '17002', '2026-03-05'),
        ]
        cur.executemany('INSERT INTO tasks (project_id, title, description, assigned_email, stage, task_type, deadline, milestone, sprint, category, status, ticket_number, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', demo_tasks)

    cur.execute('SELECT COUNT(*) FROM task_changes')
    if cur.fetchone()[0] == 0:
        changes = [
            (1, 'Guillermo Brito Acuña', 'Fecha límite: 17 de diciembre de 2025 → 31 de enero de 2026', '2026-01-07'),
            (1, 'Guillermo Brito Acuña', 'Etapa: *Pendientes/Detenidas* → *Backlog*', '2026-01-06'),
            (1, 'Henry Raúl González Brito', 'Creación de la tarea con ID 16985 y asignación inicial a Leandro', '2025-12-11'),
        ]
        cur.executemany('INSERT INTO task_changes (task_id, author, note, changed_at) VALUES (?,?,?,?)', changes)
    conn.commit()
    conn.close()

    # table to map allowed projects per user
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS user_allowed_projects (
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, project_id)
    )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = 'dev-secret-change-me'

STAGE_OPTIONS = [
    ('backlog', 'Backlog'),
    ('pending', 'Pendientes/Detenidas'),
    ('inprogress', 'En progreso'),
    ('qa', 'QA'),
    ('validation', 'Validación'),
    ('deployed', 'Desplegada'),
]
STATUS_OPTIONS = [
    ('Pendiente', 'Pendiente'),
    ('En progreso', 'En progreso'),
    ('QA', 'QA'),
    ('Validación', 'Validación'),
    ('Desplegada', 'Desplegada'),
]

STAGE_STATUS_MAP = {
    'backlog': 'Pendiente',
    'pending': 'Pendiente',
    'inprogress': 'En progreso',
    'qa': 'QA',
    'validation': 'Validación',
    'deployed': 'Desplegada',
}

CATEGORY_OPTIONS = [
    ('Codificación', 'Codificación'),
    ('Análisis', 'Análisis'),
]

def status_for_stage(stage):
    return STAGE_STATUS_MAP.get(stage, 'Pendiente')

# Ensure DB initialized at import time to avoid decorator compatibility issues
init_db()


def get_user(email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, email, password FROM users WHERE email=?', (email,))
    row = cur.fetchone()
    conn.close()
    return row


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')
        user = get_user(email)
        if user and check_password_hash(user[2], password):
            session['user'] = user[1]
            flash('Inicio de sesión correcto', 'success')
            return redirect(url_for('apps'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('apps'))


@app.route('/apps')
def apps():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Only show specific modules: Users (for admin) and Project (for all)
    user_email = session.get('user')
    modules = []
    if user_email == 'admin@example.com':
        modules.append(('Usuarios','users'))
    # Project module available to everyone
    modules.append(('Proyecto','project'))
    return render_template('apps.html', modules=modules, user=session.get('user'))


@app.route('/app/<name>')
def open_app(name):
    if 'user' not in session:
        return redirect(url_for('login'))
    # Special-case the project module to show projects list with filters
    if name == 'project':
        # get filter param
        filter_by = request.args.get('filter', 'all')
        user_email = session.get('user')
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if filter_by == 'assigned':
            cur.execute("SELECT id, name, owner_email, assigned_emails, tasks_count, tickets_count FROM projects WHERE assigned_emails LIKE ? OR owner_email = ?",('%' + user_email + '%', user_email))
        else:
            cur.execute('SELECT id, name, owner_email, assigned_emails, tasks_count, tickets_count FROM projects')
        projects = [dict(id=r[0], name=r[1], owner=r[2], assigned=r[3], tasks=r[4], tickets=r[5]) for r in cur.fetchall()]
        conn.close()
        return render_template('project_list.html', projects=projects, filter_by=filter_by)
    # Users module: admin-only creation and project assignment
    if name == 'users':
        user_email = session.get('user')
        if user_email != 'admin@example.com':
            # non-admins see placeholder
            return render_template('app_page.html', name='users')
        # admin: list users and their allowed projects
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT id, email FROM users')
        users = [dict(id=r[0], email=r[1]) for r in cur.fetchall()]
        cur.execute('SELECT id, name FROM projects')
        projects = [dict(id=r[0], name=r[1]) for r in cur.fetchall()]
        # fetch allowed projects map
        allowed = {}
        for u in users:
            cur.execute('SELECT project_id FROM user_allowed_projects WHERE user_id=?', (u['id'],))
            allowed[u['id']] = [r[0] for r in cur.fetchall()]
        conn.close()
        return render_template('users.html', users=users, projects=projects, allowed=allowed)
    return render_template('app_page.html', name=name)


@app.route('/project/<int:project_id>')
def project_detail(project_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, name, owner_email, assigned_emails, tasks_count, tickets_count FROM projects WHERE id=?', (project_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return redirect(url_for('open_app', name='project'))
    project = dict(id=row[0], name=row[1], owner=row[2], assigned=row[3].split(','), tasks=row[4], tickets=row[5])
    cur.execute('SELECT id, title, assigned_email, stage, task_type, deadline, milestone, sprint, category, status, ticket_number FROM tasks WHERE project_id=?', (project_id,))
    tasks = [dict(id=r[0], title=r[1], assigned=r[2], stage=r[3], task_type=r[4], deadline=r[5], milestone=r[6], sprint=r[7], category=r[8], status=r[9], ticket=r[10]) for r in cur.fetchall()]
    conn.close()
    task_columns = {'pending': [], 'backlog': [], 'inprogress': [], 'qa': [], 'validation': [], 'deployed': []}
    for task in tasks:
        task_columns.get(task['stage'], task_columns['backlog']).append(task)
    return render_template('project_detail.html', project=project, task_columns=task_columns)


@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task_detail(task_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, project_id, title, description, assigned_email, stage, task_type, deadline, milestone, sprint, category, status, ticket_number FROM tasks WHERE id=?', (task_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return redirect(url_for('open_app', name='project'))
    task = dict(id=row[0], project_id=row[1], title=row[2], description=row[3], assigned_email=row[4], stage=row[5], task_type=row[6], deadline=row[7], milestone=row[8], sprint=row[9], category=row[10], status=row[11], ticket_number=row[12])
    task['status'] = status_for_stage(task['stage'])
    task['stage_label'] = next((label for value,label in STAGE_OPTIONS if value == task['stage']), task['stage'])
    cur.execute('SELECT name, assigned_emails FROM projects WHERE id=?', (task['project_id'],))
    project_row = cur.fetchone()
    task['project_name'] = project_row[0] if project_row else 'Proyecto'
    project_users = project_row[1].split(',') if project_row and project_row[1] else []
    cur.execute('SELECT id, email FROM users')
    users = [dict(id=r[0], email=r[1]) for r in cur.fetchall() if r[1] in project_users]
    cur.execute('SELECT author, note, changed_at FROM task_changes WHERE task_id=? ORDER BY changed_at DESC', (task_id,))
    changes = [dict(author=r[0], note=r[1], changed_at=r[2]) for r in cur.fetchall()]

    if request.method == 'POST':
        if request.form.get('stage'):
            selected_stage = request.form.get('stage')
            stage_map = dict(STAGE_OPTIONS)
            if selected_stage in stage_map and selected_stage != task['stage']:
                new_status = status_for_stage(selected_stage)
                cur.execute('UPDATE tasks SET stage=?, status=? WHERE id=?',
                            (selected_stage, new_status, task_id))
                note = f"Etapa: *{task['stage']}* → *{selected_stage}*"
                cur.execute('INSERT INTO task_changes (task_id, author, note, changed_at) VALUES (?,?,?,datetime("now"))',
                            (task_id, session.get('user'), note))
                conn.commit()
                conn.close()
                return redirect(url_for('task_detail', task_id=task_id))
        action = request.form.get('action')
        if action == 'copy':
            copy_user = request.form.get('copy_user')
            if copy_user:
                new_ticket = f"{task['ticket_number']}-C"
                cur.execute('INSERT INTO tasks (project_id, title, description, assigned_email, stage, task_type, deadline, milestone, sprint, category, status, ticket_number, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime("now"))',
                            (task['project_id'], task['title'], task['description'], copy_user, 'backlog', task['task_type'], task['deadline'], task['milestone'], task['sprint'], task['category'], 'Pendiente', new_ticket))
                conn.commit()
                new_id = cur.lastrowid
                conn.close()
                return redirect(url_for('task_detail', task_id=new_id))
        elif action == 'save':
            fields = {
                'title': request.form.get('title', task['title']).strip(),
                'ticket_number': request.form.get('ticket_number', task['ticket_number']).strip(),
                'description': request.form.get('description', task['description']).strip(),
                'assigned_email': request.form.get('assigned_email', task['assigned_email']),
                'task_type': request.form.get('task_type', task['task_type']).strip(),
                'deadline': request.form.get('deadline', task['deadline']).strip(),
                'milestone': request.form.get('milestone', task['milestone']).strip(),
                'sprint': request.form.get('sprint', task['sprint']).strip(),
                'category': request.form.get('category', task['category']).strip(),
                'stage': task['stage'],
                'status': status_for_stage(task['stage']),
            }
            notes = []
            for key, new_value in fields.items():
                old_value = task.get(key) or ''
                if new_value != old_value:
                    field_label = {
                        'title': 'Título',
                        'ticket_number': 'ID de tarea',
                        'description': 'Descripción',
                        'assigned_email': 'Asignado a',
                        'task_type': 'Tipo',
                        'deadline': 'Fecha límite',
                        'milestone': 'Hito',
                        'sprint': 'Sprint',
                        'category': 'Categoría',
                    }.get(key, key)
                    notes.append(f"{field_label}: {old_value or 'vacío'} → {new_value or 'vacío'}")
            if notes:
                cur.execute('UPDATE tasks SET title=?, ticket_number=?, description=?, assigned_email=?, task_type=?, deadline=?, milestone=?, sprint=?, category=?, status=? WHERE id=?',
                            (fields['title'], fields['ticket_number'], fields['description'], fields['assigned_email'], fields['task_type'], fields['deadline'], fields['milestone'], fields['sprint'], fields['category'], fields['status'], task_id))
                for note in notes:
                    cur.execute('INSERT INTO task_changes (task_id, author, note, changed_at) VALUES (?,?,?,datetime("now"))',
                                (task_id, session.get('user'), note))
                conn.commit()
                conn.close()
                return redirect(url_for('task_detail', task_id=task_id))
    conn.close()
    return render_template('task_detail.html', task=task, users=users, changes=changes, stage_options=STAGE_OPTIONS, status_options=STATUS_OPTIONS)


@app.route('/app/users/create', methods=['POST'])
def create_user_route():
    if 'user' not in session or session.get('user') != 'admin@example.com':
        return redirect(url_for('login'))
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        flash('Email y contraseña requeridos', 'danger')
        return redirect(url_for('open_app', name='users'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, generate_password_hash(password)))
        conn.commit()
        flash('Usuario creado', 'success')
    except Exception as e:
        flash(f'Error al crear usuario: {e}', 'danger')
    conn.close()
    return redirect(url_for('open_app', name='users'))


@app.route('/app/users/<int:user_id>/projects', methods=['GET', 'POST'])
def edit_user_projects(user_id):
    if 'user' not in session or session.get('user') != 'admin@example.com':
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, email FROM users WHERE id=?', (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('open_app', name='users'))
    user = dict(id=row[0], email=row[1])
    cur.execute('SELECT id, name FROM projects')
    projects = [dict(id=r[0], name=r[1]) for r in cur.fetchall()]
    if request.method == 'POST':
        selected = request.form.getlist('projects')
        # replace mapping
        cur.execute('DELETE FROM user_allowed_projects WHERE user_id=?', (user_id,))
        for pid in selected:
            try:
                cur.execute('INSERT INTO user_allowed_projects (user_id, project_id) VALUES (?,?)', (user_id, int(pid)))
            except Exception:
                pass
        conn.commit()
        conn.close()
        flash('Permisos de proyecto actualizados', 'success')
        return redirect(url_for('open_app', name='users'))
    # GET: show form
    cur.execute('SELECT project_id FROM user_allowed_projects WHERE user_id=?', (user_id,))
    allowed = [r[0] for r in cur.fetchall()]
    conn.close()
    return render_template('user_edit.html', user=user, projects=projects, allowed=allowed)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        # In a real app, send reset email. Here we just flash.
        flash(f'Se ha enviado un enlace de restablecimiento a {email}', 'info')
        return redirect(url_for('login'))
    return render_template('reset.html')


@app.route('/superuser')
def superuser():
    # In Odoo this opens a superuser login; here we just show a small form.
    return render_template('superuser.html')


if __name__ == '__main__':
    app.run(debug=True, port=8018)
