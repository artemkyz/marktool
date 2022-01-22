from flask import Blueprint, render_template


bp = Blueprint('errors', __name__, template_folder='templates')


@bp.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html', err='Страница не найдена')


@bp.app_errorhandler(500)
def handle_500(err):
    return '500', 500
