from flask import Blueprint, render_template, current_app


bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/')
def home():
    current_app.logger.info('Info level log')
    current_app.logger.warning('Warning level log')
    """Show home page"""
    return render_template('home.html')
