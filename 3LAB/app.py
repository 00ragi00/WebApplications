from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'
application = app

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


USERS = {
    1: User(1, 'user', 'qwerty'),
}


@login_manager.user_loader
def load_user(user_id):
    return USERS.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/counter')
def counter():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('counter.html', visits=session['visits'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = next((u for u in USERS.values() if u.username == username), None)
        if user and user.password == password:
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))

        flash('Неверный логин или пароль.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


if __name__ == '__main__':
    app.run(debug=True)
