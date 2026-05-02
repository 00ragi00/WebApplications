import re
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'supersecretkey'
application = app


def validate_phone(raw):
    """
    Возвращает (error_message | None, formatted | None)
    """
    allowed = re.compile(r'^[\d\s()\-\.+]+$')
    if not allowed.match(raw):
        return 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.', None

    digits = re.sub(r'\D', '', raw)

    starts_with_plus7 = raw.lstrip().startswith('+7')
    starts_with_8 = digits.startswith('8')

    if starts_with_plus7 or starts_with_8:
        required = 11
    else:
        required = 10

    if len(digits) != required:
        return 'Недопустимый ввод. Неверное количество цифр.', None

    last10 = digits[-10:]
    formatted = f'8-{last10[0:3]}-{last10[3:6]}-{last10[6:8]}-{last10[8:10]}'
    return None, formatted


@app.route('/')
def index():
    return render_template('index.html')


# URL-параметры 
@app.route('/url-params')
def url_params():
    params = request.args.to_dict(flat=False)
    return render_template('url_params.html', params=params)


# Заголовки запроса 
@app.route('/headers')
def headers():
    hdrs = dict(request.headers)
    return render_template('headers.html', headers=hdrs)


# Cookie 
@app.route('/cookies', methods=['GET', 'POST'])
def cookies():
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'set':
            name  = request.form.get('cname', '').strip()
            value = request.form.get('cvalue', '').strip()
            resp  = make_response(redirect(url_for('cookies')))
            if name:
                resp.set_cookie(name, value)
                message = f'Cookie «{name}» установлен.'
            return resp
        elif action == 'delete':
            name = request.form.get('del_name', '').strip()
            resp = make_response(redirect(url_for('cookies')))
            if name:
                resp.delete_cookie(name)
                message = f'Cookie «{name}» удалён.'
            return resp

    all_cookies = dict(request.cookies)
    return render_template('cookies.html', cookies=all_cookies, message=message)


# Параметры формы (авторизация) 
@app.route('/form-data', methods=['GET', 'POST'])
def form_data():
    submitted = None
    if request.method == 'POST':
        submitted = {
            'Логин':  request.form.get('username', ''),
            'Пароль': request.form.get('password', ''),
        }
    return render_template('form_data.html', submitted=submitted)


# Валидация телефона 
@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error     = None
    formatted = None
    raw       = ''

    if request.method == 'POST':
        raw = request.form.get('phone', '').strip()
        if raw:
            error, formatted = validate_phone(raw)
        else:
            error = 'Недопустимый ввод. Неверное количество цифр.'

    return render_template('phone.html', error=error, formatted=formatted, raw=raw)


if __name__ == '__main__':
    app.run(debug=True)
