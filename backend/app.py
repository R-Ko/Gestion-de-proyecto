"""
API Backend - Flask app para Render
Conecta con Aiven/PostgreSQL o MySQL
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
import ssl
import time
import urllib.parse as urlparse
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:
    pymysql = None

load_dotenv()

# Configuración
BASE_DIR = Path(__file__).parent
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no configurada. Usa postgresql://... o mysql://...")

parsed_db_url = urlparse.urlparse(DATABASE_URL)
DB_ENGINE = None
if parsed_db_url.scheme in ('postgres', 'postgresql'):
    DB_ENGINE = 'postgres'
elif parsed_db_url.scheme == 'mysql':
    DB_ENGINE = 'mysql'
else:
    raise ValueError(f"Esquema de DATABASE_URL no soportado: {parsed_db_url.scheme}")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

# Habilitar CORS para que el frontend acceda desde GitHub Pages
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://tu-usuario.github.io",
            "http://localhost:3000",
            "http://localhost:8080"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


def now_timestamp():
    return datetime.now().isoformat()


def connect_db():
    """Conectar a Postgres o MySQL según DATABASE_URL."""
    if DB_ENGINE == 'postgres':
        if psycopg2 is None:
            raise RuntimeError('psycopg2-binary es requerido')
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

    if DB_ENGINE == 'mysql':
        if pymysql is None:
            raise RuntimeError('pymysql es requerido para MySQL')

        query_params = dict(urlparse.parse_qsl(parsed_db_url.query))
        ssl_args = None
        ssl_mode = query_params.get('ssl-mode') or query_params.get('sslmode')
        if ssl_mode and ssl_mode.lower() in ('required', 'require', 'true', '1'):
            ssl_args = {'ssl': {}}

        return pymysql.connect(
            host=parsed_db_url.hostname,
            port=parsed_db_url.port or 3306,
            user=parsed_db_url.username,
            password=parsed_db_url.password,
            database=parsed_db_url.path.lstrip('/'),
            charset='utf8mb4',
            cursorclass=DictCursor,
            ssl=ssl_args,
            autocommit=False
        )

    raise RuntimeError('Motor de base de datos desconocido')


def db_execute(conn, query, params=None):
    """Ejecutar query sin retorno"""
    if params is None:
        params = ()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()


def db_fetch(conn, query, params=None):
    """Obtener resultado de query"""
    if params is None:
        params = ()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    return result


def db_fetch_one(conn, query, params=None):
    """Obtener un resultado de query"""
    if params is None:
        params = ()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    cur.close()
    return result


def init_db():
    """Inicializar base de datos en Supabase"""
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        user_id_type = 'SERIAL PRIMARY KEY' if DB_ENGINE == 'postgres' else 'INT PRIMARY KEY AUTO_INCREMENT'
        timestamp_default = 'TIMESTAMP DEFAULT NOW()' if DB_ENGINE == 'postgres' else 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        foreign_key_syntax = 'REFERENCES projects(id)' if DB_ENGINE == 'postgres' else 'REFERENCES projects(id)'

        # Crear tabla users
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS users (
            id {user_id_type},
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at {timestamp_default}
        )
        ''')
        
        # Crear tabla projects
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS projects (
            id {user_id_type},
            name TEXT NOT NULL,
            owner_email TEXT,
            assigned_emails TEXT,
            tasks_count INTEGER DEFAULT 0,
            tickets_count INTEGER DEFAULT 0,
            created_at {timestamp_default}
        )
        ''')
        
        # Crear tabla tasks
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            id {user_id_type},
            project_id INTEGER NOT NULL {foreign_key_syntax},
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
            created_at {timestamp_default}
        )
        ''')
        
        # Crear tabla task_changes (auditoría)
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS task_changes (
            id {user_id_type},
            task_id INTEGER NOT NULL REFERENCES tasks(id),
            author TEXT,
            note TEXT,
            changed_at {timestamp_default}
        )
        ''')
        
        # Crear tabla user_allowed_projects (control de acceso)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_allowed_projects (
            user_id INTEGER NOT NULL REFERENCES users(id),
            project_id INTEGER NOT NULL REFERENCES projects(id),
            PRIMARY KEY (user_id, project_id)
        )
        ''')
        
        conn.commit()
        print("✓ Tablas creadas/verificadas en Supabase")
        
    except Exception as e:
        print(f"Error inicializando DB: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# ============================================================================
# RUTAS API - AUTENTICACIÓN
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'message': 'API funcionando'}), 200


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login API - Retorna token de sesión"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email y contraseña requeridos'}), 400
    
    conn = connect_db()
    user = db_fetch_one(conn, 'SELECT id, email, password FROM users WHERE email = %s', (email,))
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user'] = user['email']
        session['user_id'] = user['id']
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'user': user['email']
        }), 200
    
    return jsonify({'error': 'Credenciales inválidas'}), 401


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout API"""
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada'}), 200


@app.route('/api/user', methods=['GET'])
def api_get_user():
    """Obtener usuario autenticado actual"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    return jsonify({
        'email': session.get('user'),
        'user_id': session.get('user_id')
    }), 200


# ============================================================================
# RUTAS API - PROYECTOS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def api_get_projects():
    """Obtener proyectos del usuario"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    conn = connect_db()
    projects = db_fetch(conn, '''
        SELECT p.* FROM projects p
        WHERE p.owner_email = %s OR p.assigned_emails LIKE %s
        ORDER BY p.created_at DESC
    ''', (session.get('user'), f"%{session.get('user')}%"))
    conn.close()
    
    return jsonify([dict(p) for p in projects]), 200


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def api_get_project(project_id):
    """Obtener detalle de proyecto"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    conn = connect_db()
    project = db_fetch_one(conn, 'SELECT * FROM projects WHERE id = %s', (project_id,))
    conn.close()
    
    if not project:
        return jsonify({'error': 'Proyecto no encontrado'}), 404
    
    return jsonify(dict(project)), 200


@app.route('/api/projects', methods=['POST'])
def api_create_project():
    """Crear nuevo proyecto"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Nombre de proyecto requerido'}), 400
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        if DB_ENGINE == 'postgres':
            cur.execute('''
                INSERT INTO projects (name, owner_email, assigned_emails)
                VALUES (%s, %s, %s)
                RETURNING id, name, owner_email, assigned_emails
            ''', (name, session.get('user'), session.get('user')))
            result = cur.fetchone()
        else:
            cur.execute('''
                INSERT INTO projects (name, owner_email, assigned_emails)
                VALUES (%s, %s, %s)
            ''', (name, session.get('user'), session.get('user')))
            project_id = cur.lastrowid
            conn.commit()
            result = db_fetch_one(conn, 'SELECT id, name, owner_email, assigned_emails FROM projects WHERE id = %s', (project_id,))

        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Proyecto creado',
            'project': {
                'id': result[0] if DB_ENGINE == 'postgres' else result['id'],
                'name': result[1] if DB_ENGINE == 'postgres' else result['name'],
                'owner_email': result[2] if DB_ENGINE == 'postgres' else result['owner_email'],
                'assigned_emails': result[3] if DB_ENGINE == 'postgres' else result['assigned_emails']
            }
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ============================================================================
# RUTAS API - TAREAS
# ============================================================================

@app.route('/api/projects/<int:project_id>/tasks', methods=['GET'])
def api_get_tasks(project_id):
    """Obtener tareas de un proyecto"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    conn = connect_db()
    tasks = db_fetch(conn, '''
        SELECT t.* FROM tasks t
        WHERE t.project_id = %s
        ORDER BY t.created_at DESC
    ''', (project_id,))
    conn.close()
    
    return jsonify([dict(t) for t in tasks]), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    """Obtener detalle de tarea"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    conn = connect_db()
    task = db_fetch_one(conn, 'SELECT * FROM tasks WHERE id = %s', (task_id,))
    
    if not task:
        conn.close()
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    # Obtener historial de cambios
    changes = db_fetch(conn, '''
        SELECT * FROM task_changes WHERE task_id = %s
        ORDER BY changed_at DESC
    ''', (task_id,))
    
    conn.close()
    
    return jsonify({
        **dict(task),
        'changes': [dict(c) for c in changes]
    }), 200


@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """Crear nueva tarea"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    data = request.get_json()
    project_id = data.get('project_id')
    title = data.get('title')
    
    if not project_id or not title:
        return jsonify({'error': 'project_id y title requeridos'}), 400
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        if DB_ENGINE == 'postgres':
            cur.execute('''
                INSERT INTO tasks 
                (project_id, title, description, assigned_email, stage, task_type, deadline, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, title, project_id
            ''', (
                project_id,
                title,
                data.get('description', ''),
                data.get('assigned_email', session.get('user')),
                data.get('stage', 'backlog'),
                data.get('task_type', 'Codificación'),
                data.get('deadline', ''),
                data.get('status', 'Pendiente'),
                now_timestamp(),
            ))
            result = cur.fetchone()
        else:
            cur.execute('''
                INSERT INTO tasks 
                (project_id, title, description, assigned_email, stage, task_type, deadline, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                project_id,
                title,
                data.get('description', ''),
                data.get('assigned_email', session.get('user')),
                data.get('stage', 'backlog'),
                data.get('task_type', 'Codificación'),
                data.get('deadline', ''),
                data.get('status', 'Pendiente'),
                now_timestamp(),
            ))
            task_id = cur.lastrowid
            conn.commit()
            result = db_fetch_one(conn, 'SELECT id, title, project_id FROM tasks WHERE id = %s', (task_id,))

        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea creada',
            'task': {
                'id': result[0] if DB_ENGINE == 'postgres' else result['id'],
                'title': result[1] if DB_ENGINE == 'postgres' else result['title'],
                'project_id': result[2] if DB_ENGINE == 'postgres' else result['project_id']
            }
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/api/tasks/<int:task_id>/stage', methods=['PUT'])
def api_update_task_stage(task_id):
    """Cambiar stage de una tarea"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    data = request.get_json()
    new_stage = data.get('stage')
    note = data.get('note', f'Cambio de estado a {new_stage}')
    
    if not new_stage:
        return jsonify({'error': 'stage requerido'}), 400
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # Actualizar stage
        cur.execute('UPDATE tasks SET stage = %s WHERE id = %s', (new_stage, task_id))
        
        # Registrar cambio en auditoría
        cur.execute('''
            INSERT INTO task_changes (task_id, author, note, changed_at)
            VALUES (%s, %s, %s, %s)
        ''', (task_id, session.get('user'), note, now_timestamp()))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': f'Tarea actualizada a {new_stage}'
        }), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

if __name__ == '__main__':
    init_db()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
