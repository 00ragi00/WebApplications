import csv
import io
from flask import Blueprint, render_template, request, Response
from utils import get_db, get_current_user, check_rights

reports_bp = Blueprint('reports', __name__, url_prefix='/logs')

PER_PAGE = 10


def _fullname(row):
    parts = [p for p in (row['last_name'], row['first_name'], row['middle_name']) if p]
    return ' '.join(parts) if parts else 'Неаутентифицированный пользователь'


@reports_bp.route('/')
@check_rights('view_logs')
def logs_index():
    user = get_current_user()
    is_admin = user['role_name'] == 'Администратор'

    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1

    db = get_db()
    if is_admin:
        total = db.execute("SELECT COUNT(*) FROM visit_logs").fetchone()[0]
        logs = db.execute(
            """SELECT vl.id, vl.path, vl.created_at, vl.user_id,
                      u.last_name, u.first_name, u.middle_name
               FROM visit_logs vl
               LEFT JOIN users u ON vl.user_id = u.id
               ORDER BY vl.created_at DESC
               LIMIT ? OFFSET ?""",
            (PER_PAGE, (page - 1) * PER_PAGE)
        ).fetchall()
    else:
        total = db.execute(
            "SELECT COUNT(*) FROM visit_logs WHERE user_id = ?",
            (user['id'],)
        ).fetchone()[0]
        logs = db.execute(
            """SELECT vl.id, vl.path, vl.created_at, vl.user_id,
                      u.last_name, u.first_name, u.middle_name
               FROM visit_logs vl
               LEFT JOIN users u ON vl.user_id = u.id
               WHERE vl.user_id = ?
               ORDER BY vl.created_at DESC
               LIMIT ? OFFSET ?""",
            (user['id'], PER_PAGE, (page - 1) * PER_PAGE)
        ).fetchall()
    db.close()

    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    return render_template(
        'logs/index.html',
        logs=logs,
        page=page,
        pages=pages,
        per_page=PER_PAGE,
        is_admin=is_admin,
    )


@reports_bp.route('/pages')
@check_rights('view_stats')
def logs_by_page():
    db = get_db()
    stats = db.execute(
        """SELECT path, COUNT(*) AS cnt
           FROM visit_logs
           GROUP BY path
           ORDER BY cnt DESC"""
    ).fetchall()
    db.close()
    return render_template('logs/by_page.html', stats=stats)


@reports_bp.route('/pages/export')
@check_rights('view_stats')
def logs_by_page_export():
    db = get_db()
    stats = db.execute(
        """SELECT path, COUNT(*) AS cnt
           FROM visit_logs
           GROUP BY path
           ORDER BY cnt DESC"""
    ).fetchall()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Страница', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        writer.writerow([i, row['path'], row['cnt']])

    content = '' + output.getvalue()
    return Response(
        content.encode('utf-8'),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=pages_report.csv'},
    )


@reports_bp.route('/users')
@check_rights('view_stats')
def logs_by_user():
    db = get_db()
    stats = db.execute(
        """SELECT vl.user_id, u.last_name, u.first_name, u.middle_name,
                  COUNT(*) AS cnt
           FROM visit_logs vl
           LEFT JOIN users u ON vl.user_id = u.id
           GROUP BY vl.user_id
           ORDER BY cnt DESC"""
    ).fetchall()
    db.close()
    return render_template('logs/by_user.html', stats=stats)


@reports_bp.route('/users/export')
@check_rights('view_stats')
def logs_by_user_export():
    db = get_db()
    stats = db.execute(
        """SELECT vl.user_id, u.last_name, u.first_name, u.middle_name,
                  COUNT(*) AS cnt
           FROM visit_logs vl
           LEFT JOIN users u ON vl.user_id = u.id
           GROUP BY vl.user_id
           ORDER BY cnt DESC"""
    ).fetchall()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        writer.writerow([i, _fullname(row), row['cnt']])

    content = '' + output.getvalue()
    return Response(
        content.encode('utf-8'),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=users_report.csv'},
    )
