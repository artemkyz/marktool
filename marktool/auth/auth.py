from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
import uuid
from marktool.app_utils.mailer import send_mail
from marktool.config import SERVICE_EMAIL
from marktool.models import User, db, UserTemp


bp = Blueprint('auth', __name__, template_folder='templates')


@bp.route('/registration', methods=['GET', 'POST'])
# @bp.route('/registration', methods=['POST'])

def registration():
    if request.method == 'POST':
        date = datetime.now().timestamp()
        gln = request.form['gln']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not gln:
            error = 'Требуется GLN'
        elif not password:
            error = 'Требуется пароль'

        if error is None:
            user = db.session.query(User).filter(User.gln == gln).first()
            if user:
                error = '<p style="color:green; text-align:center; margin:0;">Пользователь с таким GLN уже ' \
                          'зарегистрирован, <a href="/login">войти</a>?</p> '

            elif user is None:
                token = uuid.uuid4().hex
                user = UserTemp(date=date, gln=gln, password=generate_password_hash(password), email=email, token=token)
                db.session.add(user)
                db.session.commit()
                # send_registration(email, token)
                message = f'<p style="text-align:center; margin:0;">Для завершения регистрации ' \
                          f'проверьте почту {email} и перейдите по ссылке в письме</p> '
                return render_template('login.html', message=message)

        flash(error)
    return redirect(url_for('home'))


@bp.route('/confirm_registration', methods=['GET'])
def confirm_registration():
    user_token = request.args.get('token')

    if user_token:
        user = db.session.query(UserTemp).filter(UserTemp.token == user_token).first()
        if user:
            date_diff = datetime.now().timestamp() - float(user.date)  # с момента регистрации должно пройти не
            # больше 86400 секунд (24 часа)
            if date_diff < 86400:
                new_user = User(date=user.date, gln=user.gln, password=user.password, email=user.email)
                db.session.add(new_user)
                db.session.commit()

                db.session.delete(user)
                db.session.commit()
                message = f'<p style="color:green; text-align:center; margin:0;">Регистрация успешно завершена.<br> ' \
                          f'Используйте номер GLN и пароль для входа в систему</p> '
                return render_template('login.html', message=message)

            db.session.delete(user)
            db.session.commit()
            message = f'<p style="color:green; text-align:center; margin:0;">Срок подтверждения регистрации истёк.' \
                      f'<br>Повторите регистрацию снова</p> '

            return render_template('registration.html', message=message)

    return "refused by server", 200


@bp.route('/login', methods=['GET', 'POST'])
# @bp.route('/login', methods=['POST'])
def login():
    # if request.method == 'GET':
    #     try:
    #         if session['gln']:  # сессия есть - редирект в ЛК
    #             return redirect(url_for('area'))
    #     except KeyError:
    #         return render_template('login.html')  # сессии нет - страница входа

    if request.method == 'POST':
        gln = request.form['gln']
        password = request.form['password']
        user = db.session.query(User).filter(User.gln == gln).first()
        error = None

        if user is None:
            error = '<p style="text-align:center; margin:0; color:red;">Неверный GLN<p>'

        elif not check_password_hash(user.password, password):
            error = '<p style="text-align:center; margin:0; color:red;">Неверный пароль<p>'

        if error is None:
            session['gln'] = request.form['gln']
            return redirect(url_for('area'))

        flash(error)
    # return render_template('login.html')
    return redirect(url_for('home'))


@bp.route('/logout')
def delete_gln():
    session.pop('gln', default=None)
    return redirect(url_for('home'))


def send_registration(email, token):
    send_mail(send_from=SERVICE_EMAIL, send_to=[email], subject='Регистрация Маркировка',
              text=f'''Для подтверждения регистрации на сайте mark-tool перейдите по ссылке 
{url_for("confirm_registration", token=token)} 
В случае если это письмо ошибочно попало в Ваш почтовый ящик просто удалите его.''')
