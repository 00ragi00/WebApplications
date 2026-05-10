from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from functools import wraps
import sqlite3
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lab4.db')

# DB

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
        with open(schema_path, encoding='utf-8') as f:
            db.executescript(f.read())
        # create real admin hash
        admin = db.execute("SELECT id, password_hash FROM users WHERE login='admin'").fetchone()
        if admin and 'placeholder' in admin['password_hash']:
            h = generate_password_hash('Admin123!')
            db.execute("UPDATE users SET password_hash=? WHERE id=?", (h, admin['id']))
        db.commit()
        db.close()

# Validation

ALLOWED_SPECIAL = r'~!?@#$%^&*_\-+()\[\]{}<>/\\|"\'\.,;:'

def validate_login(login):
    if not login:
        return 'Поле не может быть пустым'
    if len(login) < 5:
        return 'Логин должен содержать не менее 5 символов'
    if not re.fullmatch(r'[A-Za-z0-9]+', login):
        return 'Логин должен состоять только из латинских букв и цифр'
    return None


def validate_password(password):
    if not password:
        return 'Поле не может быть пустым'
    if len(password) < 8:
        return 'Пароль должен содержать не менее 8 символов'
    if len(password) > 128:
        return 'Пароль не должен превышать 128 символов'
    if ' ' in password:
        return 'Пароль не должен содержать пробелы'
    if not re.search(r'[A-ZА-ЯЁ]', password):
        return 'Пароль должен содержать хотя бы одну заглавную букву'
    if not re.search(r'[a-zа-яё]', password):
        return 'Пароль должен содержать хотя бы одну строчную букву'
    if not re.search(r'[0-9]', password):
        return 'Пароль должен содержать хотя бы одну цифру'
    allowed_pattern = r'^[A-Za-zА-ЯЁа-яё0-9' + ALLOWED_SPECIAL + r']+$'
    if not re.fullmatch(allowed_pattern, password):
        return 'Пароль содержит недопустимые символы'
    return None


def validate_user_form(form, check_password=True):
    errors = {}
    if check_password:
        err = validate_login(form.get('login', '').strip())
        if err:
            errors['login'] = err
        err = validate_password(form.get('password', ''))
        if err:
            errors['password'] = err
    if not form.get('first_name', '').strip():
        errors['first_name'] = 'Поле не может быть пустым'
    return errors


# Auth

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа к этой странице необходимо войти в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    if 'user_id' not in session:
        return None
    db = get_db()
    user = db.execute(
        "SELECT u.*, r.name AS role_name FROM users u LEFT JOIN roles r ON u.role_id = r.id WHERE u.id = ?",
        (session['user_id'],)
    ).fetchone()
    db.close()
    return user

@app.context_processor
def inject_user():
    return {'current_user': get_current_user()}

# Auth routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE login = ?", (login_val,)).fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Main page

@app.route('/')
def index():
    db = get_db()
    users = db.execute(
        """SELECT u.id, u.login, u.last_name, u.first_name, u.middle_name,
                  r.name AS role_name
           FROM users u
           LEFT JOIN roles r ON u.role_id = r.id
           ORDER BY u.id"""
    ).fetchall()
    db.close()
    return render_template('index.html', users=users)

# View user

@app.route('/users/<int:user_id>')
def user_view(user_id):
    db = get_db()
    user = db.execute(
        """SELECT u.*, r.name AS role_name
           FROM users u LEFT JOIN roles r ON u.role_id = r.id
           WHERE u.id = ?""",
        (user_id,)
    ).fetchone()
    db.close()
    if not user:
        abort(404)
    return render_template('user_view.html', user=user)


# Create user

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
def user_create():
    db = get_db()
    roles = db.execute("SELECT * FROM roles ORDER BY name").fetchall()

    if request.method == 'POST':
        form = request.form
        errors = validate_user_form(form, check_password=True)

        if errors:
            db.close()
            return render_template('user_create.html', roles=roles, form=form, errors=errors)

        login_val = form['login'].strip()
        password_hash = generate_password_hash(form['password'])
        last_name = form.get('last_name', '').strip() or None
        first_name = form['first_name'].strip()
        middle_name = form.get('middle_name', '').strip() or None
        role_id = form.get('role_id') or None

        try:
            db.execute(
                """INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (login_val, password_hash, last_name, first_name, middle_name, role_id)
            )
            db.commit()
            db.close()
            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            db.close()
            flash('Пользователь с таким логином уже существует', 'danger')
            errors['login'] = 'Пользователь с таким логином уже существует'
            return render_template('user_create.html', roles=roles, form=form, errors=errors)
        except Exception as e:
            db.close()
            flash(f'Ошибка при создании пользователя: {e}', 'danger')
            return render_template('user_create.html', roles=roles, form=form, errors=errors)

    db.close()
    return render_template('user_create.html', roles=roles, form={}, errors={})

# Edit user

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        db.close()
        abort(404)
    roles = db.execute("SELECT * FROM roles ORDER BY name").fetchall()

    if request.method == 'POST':
        form = request.form
        errors = validate_user_form(form, check_password=False)

        if errors:
            db.close()
            return render_template('user_edit.html', roles=roles, form=form, errors=errors, user=user)

        last_name = form.get('last_name', '').strip() or None
        first_name = form['first_name'].strip()
        middle_name = form.get('middle_name', '').strip() or None
        role_id = form.get('role_id') or None

        try:
            db.execute(
                """UPDATE users SET last_name=?, first_name=?, middle_name=?, role_id=?
                   WHERE id=?""",
                (last_name, first_name, middle_name, role_id, user_id)
            )
            db.commit()
            db.close()
            flash('Данные пользователя успешно обновлены', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.close()
            flash(f'Ошибка при обновлении данных: {e}', 'danger')
            return render_template('user_edit.html', roles=roles, form=form, errors=errors, user=user)

    form = dict(user)
    db.close()
    return render_template('user_edit.html', roles=roles, form=form, errors={}, user=user)

# Delete user

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def user_delete(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        db.close()
        abort(404)
    try:
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        db.close()
        flash('Пользователь успешно удалён', 'success')
    except Exception as e:
        db.close()
        flash(f'Ошибка при удалении пользователя: {e}', 'danger')
    return redirect(url_for('index'))

# Change password

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    errors = {}
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
        db.close()

        if not check_password_hash(user['password_hash'], old_password):
            errors['old_password'] = 'Неверный текущий пароль'

        err = validate_password(new_password)
        if err:
            errors['new_password'] = err

        if not errors and new_password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'

        if errors:
            flash('Исправьте ошибки в форме', 'danger')
            return render_template('change_password.html', errors=errors)

        new_hash = generate_password_hash(new_password)
        db = get_db()
        try:
            db.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, session['user_id']))
            db.commit()
            db.close()
            flash('Пароль успешно изменён', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.close()
            flash(f'Ошибка при смене пароля: {e}', 'danger')

    return render_template('change_password.html', errors=errors)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
