from flask import Flask, render_template, request, redirect, url_for, make_response
from urllib.parse import urlencode
import re

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('index.html')

PARAM_ROWS = 4  

@app.route('/info')
def info():
    url_params = dict(request.args)
    headers    = dict(request.headers)
    cookies    = dict(request.cookies)

    pairs = list(url_params.items())
    pairs += [('', '')] * (PARAM_ROWS - len(pairs))
    pairs = pairs[:PARAM_ROWS]
    return render_template('info.html', url_params=url_params, pairs=pairs, headers=headers, cookies=cookies)


@app.route('/apply-params', methods=['POST'])
def apply_params():
    keys = request.form.getlist('pkey')
    vals = request.form.getlist('pval')
    params = [(k.strip(), v.strip()) for k, v in zip(keys, vals) if k.strip()]
    qs = urlencode(params)
    return redirect(url_for('info') + ('?' + qs if qs else ''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    submitted = None

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        submitted = {'username': username, 'password': password}

    return render_template('login.html', submitted=submitted)

@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    name  = request.form.get('name', '').strip()
    value = request.form.get('value', '').strip()
    resp  = make_response(redirect(url_for('info')))
    if name:
        resp.set_cookie(name, value)
    return resp

@app.route('/delete-cookie', methods=['POST'])
def delete_cookie():
    name = request.form.get('name', '').strip()
    resp = make_response(redirect(url_for('info')))
    if name:
        resp.delete_cookie(name)
    return resp

def validate_phone(raw):
    bad = re.sub(r'[\d\s()\-\.+]', '', raw)
    if bad:
        return 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.', None

    digits = re.sub(r'\D', '', raw)
    stripped = raw.strip()
    if stripped.startswith('+7') or (digits and digits[0] == '8'):
        required = 11
    else:
        required = 10

    if len(digits) != required:
        return 'Недопустимый ввод. Неверное количество цифр.', None

    d = digits if len(digits) == 11 else '8' + digits
    formatted = f'8-{d[1:4]}-{d[4:7]}-{d[7:9]}-{d[9:11]}'
    return None, formatted

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_value = ''
    error = None
    formatted = None

    if request.method == 'POST':
        phone_value = request.form.get('phone', '')
        error, formatted = validate_phone(phone_value)

    return render_template('phone.html',
                           phone_value=phone_value,
                           error=error,
                           formatted=formatted)

if __name__ == '__main__':
    app.run(debug=True)
