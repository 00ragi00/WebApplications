import sqlite3
import os
from functools import wraps
from flask import session, redirect, url_for, flash

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lab4.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_current_user():
    if 'user_id' not in session:
        return None
    db = get_db()
    user = db.execute(
        """SELECT u.*, r.name AS role_name
           FROM users u LEFT JOIN roles r ON u.role_id = r.id
           WHERE u.id = ?""",
        (session['user_id'],)
    ).fetchone()
    db.close()
    return user


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа к этой странице необходимо войти в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def check_rights(right):
    """Decorator that verifies the current user has the given right.

    Rights:
      'create_user'  — Admin only
      'delete_user'  — Admin only
      'view_stats'   — Admin only (reports by page / by user)
      'edit_user'    — Admin (any) or User (own profile only)
      'view_user'    — Admin (any) or User (own profile only)
      'view_logs'    — Admin and User (content filtered in view)
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            if not user:
                flash('Для доступа к этой странице необходимо войти в систему', 'warning')
                return redirect(url_for('login'))

            role = user['role_name']
            allowed = False

            if role == 'Администратор':
                allowed = True
            elif role == 'Пользователь':
                if right in ('edit_user', 'view_user'):
                    user_id = kwargs.get('user_id')
                    allowed = (user_id == user['id'])
                elif right == 'view_logs':
                    allowed = True
                # create_user, delete_user, view_stats — not allowed for User

            if not allowed:
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))

            return f(*args, **kwargs)
        return decorated
    return decorator
