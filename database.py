import sqlite3
import bcrypt
from config import DB_PATH, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, INITIAL_APPS


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            active INTEGER NOT NULL DEFAULT 1
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            url TEXT,
            icon TEXT DEFAULT '📱',
            active INTEGER NOT NULL DEFAULT 1
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_apps (
            user_id INTEGER NOT NULL,
            app_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, app_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (app_id) REFERENCES apps(id)
        )
    """)

    conn.commit()

    # Create default admin if not exists
    c.execute("SELECT id FROM users WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    if not c.fetchone():
        password_hash = bcrypt.hashpw(
            DEFAULT_ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        c.execute(
            "INSERT INTO users (username, password_hash, role, active) VALUES (?, ?, 'admin', 1)",
            (DEFAULT_ADMIN_USERNAME, password_hash),
        )
        conn.commit()
        admin_id = c.lastrowid

        # Insert initial apps
        for app in INITIAL_APPS:
            c.execute(
                "INSERT INTO apps (name, description, url, icon, active) VALUES (?, ?, ?, ?, ?)",
                (app["name"], app["description"], app["url"], app["icon"], 1 if app["active"] else 0),
            )
            app_id = c.lastrowid
            c.execute(
                "INSERT INTO user_apps (user_id, app_id) VALUES (?, ?)",
                (admin_id, app_id),
            )
        conn.commit()

    conn.close()


# ── USER OPERATIONS ──────────────────────────────────────────────────────────

def get_user(username: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, role, active FROM users ORDER BY username")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_user(username: str, password: str, role: str = "user"):
    conn = get_connection()
    c = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, role, active) VALUES (?, ?, ?, 1)",
            (username, password_hash, role),
        )
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return new_id, None
    except sqlite3.IntegrityError:
        conn.close()
        return None, "Użytkownik o tej nazwie już istnieje."


def update_user_password(user_id: int, new_password: str):
    conn = get_connection()
    c = conn.cursor()
    password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
    conn.commit()
    conn.close()


def toggle_user_active(user_id: int, active: bool):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET active = ? WHERE id = ?", (1 if active else 0, user_id))
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM user_apps WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


# ── APP OPERATIONS ────────────────────────────────────────────────────────────

def get_all_apps():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM apps ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_apps_for_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT a.* FROM apps a
        JOIN user_apps ua ON ua.app_id = a.id
        WHERE ua.user_id = ? AND a.active = 1
        ORDER BY a.name
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_app(name: str, description: str, url: str, icon: str = "📱", active: bool = True):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO apps (name, description, url, icon, active) VALUES (?, ?, ?, ?, ?)",
        (name, description, url, icon, 1 if active else 0),
    )
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return new_id


def update_app(app_id: int, name: str, description: str, url: str, icon: str, active: bool):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE apps SET name=?, description=?, url=?, icon=?, active=? WHERE id=?",
        (name, description, url, icon, 1 if active else 0, app_id),
    )
    conn.commit()
    conn.close()


def delete_app(app_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM user_apps WHERE app_id = ?", (app_id,))
    c.execute("DELETE FROM apps WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


# ── USER-APP ASSIGNMENT ──────────────────────────────────────────────────────

def get_user_app_ids(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT app_id FROM user_apps WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [r["app_id"] for r in rows]


def set_user_apps(user_id: int, app_ids: list):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM user_apps WHERE user_id = ?", (user_id,))
    for app_id in app_ids:
        c.execute("INSERT OR IGNORE INTO user_apps (user_id, app_id) VALUES (?, ?)", (user_id, app_id))
    conn.commit()
    conn.close()
