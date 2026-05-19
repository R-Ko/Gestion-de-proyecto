"""
API Backend - Flask app para Render
Solo MySQL (Aiven)
"""

from flask import Flask, request, session, jsonify
from werkzeug.security import check_password_hash
from flask_cors import CORS
import os
import urllib.parse as urlparse
from datetime import datetime
from dotenv import load_dotenv

import pymysql
from pymysql.cursors import DictCursor

load_dotenv()

# =========================
# CONFIG
# =========================

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no configurada")

parsed_db_url = urlparse.urlparse(DATABASE_URL)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


# =========================
# DB CONNECTION (MYSQL ONLY)
# =========================

def connect_db():
    query_params = dict(urlparse.parse_qsl(parsed_db_url.query))

    ssl_args = None
    ssl_mode = query_params.get("ssl-mode") or query_params.get("sslmode")

    if ssl_mode and ssl_mode.lower() in ("required", "require", "true", "1"):
        ssl_args = {"ssl": {}}

    return pymysql.connect(
        host=parsed_db_url.hostname,
        port=parsed_db_url.port or 3306,
        user=parsed_db_url.username,
        password=parsed_db_url.password,
        database=parsed_db_url.path.lstrip("/"),
        cursorclass=DictCursor,
        charset="utf8mb4",
        ssl=ssl_args,
        autocommit=False
    )


# =========================
# HELPERS
# =========================

def now():
    return datetime.now().isoformat()


def db_fetch_one(conn, query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    res = cur.fetchone()
    cur.close()
    return res


def db_fetch(conn, query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    res = cur.fetchall()
    cur.close()
    return res


def db_execute(conn, query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()


# =========================
# HEALTH
# =========================

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


# =========================
# LOGIN
# =========================

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = connect_db()

    user = db_fetch_one(
        conn,
        "SELECT id, email, password FROM users WHERE email=%s",
        (email,)
    )

    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user"] = user["email"]
        session["user_id"] = user["id"]
        return jsonify({"ok": True, "user": user["email"]})

    return jsonify({"error": "invalid credentials"}), 401


# =========================
# PROJECTS
# =========================

@app.route("/api/projects", methods=["GET"])
def projects():
    if "user" not in session:
        return jsonify({"error": "unauthorized"}), 401

    conn = connect_db()

    rows = db_fetch(
        conn,
        """
        SELECT * FROM projects
        WHERE owner_email=%s OR assigned_emails LIKE %s
        ORDER BY created_at DESC
        """,
        (session["user"], f"%{session['user']}%")
    )

    conn.close()

    return jsonify(rows)


@app.route("/api/projects", methods=["POST"])
def create_project():
    if "user" not in session:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")

    conn = connect_db()

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO projects (name, owner_email, assigned_emails)
        VALUES (%s, %s, %s)
        """,
        (name, session["user"], session["user"])
    )

    conn.commit()
    project_id = cur.lastrowid
    cur.close()

    project = db_fetch_one(conn, "SELECT * FROM projects WHERE id=%s", (project_id,))
    conn.close()

    return jsonify(project), 201


# =========================
# TASKS
# =========================

@app.route("/api/projects/<int:project_id>/tasks")
def tasks(project_id):
    conn = connect_db()

    rows = db_fetch(
        conn,
        "SELECT * FROM tasks WHERE project_id=%s ORDER BY created_at DESC",
        (project_id,)
    )

    conn.close()
    return jsonify(rows)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks
        (project_id, title, description, assigned_email, stage, status, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            data["project_id"],
            data["title"],
            data.get("description", ""),
            session.get("user"),
            "backlog",
            "pending",
            now()
        )
    )

    conn.commit()
    task_id = cur.lastrowid
    cur.close()

    task = db_fetch_one(conn, "SELECT * FROM tasks WHERE id=%s", (task_id,))
    conn.close()

    return jsonify(task), 201


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Backend funcionando 🚀"
    })
