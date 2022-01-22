import os
from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from marktool.app_utils.mailer import send_mail
from marktool.area import unify_self_signs
from marktool.config import SERVICE_EMAIL, SERVICE_DIR
from marktool.models import db, Furs


bp = Blueprint('area', __name__, template_folder='templates')


@bp.route('/area', methods=['GET', 'POST'])
def area():
    if request.method == 'GET':
        try:
            if session['gln']:
                return render_template('area.html')
        except KeyError:
            return redirect(url_for('login'))


@bp.route('/marked', methods=['GET'])
def marked():
    gln = session['gln']
    furs = db.session.query(Furs).filter(Furs.gln == gln).all()
    if furs:
        return render_template('marked.html', furs=furs)

    message = '<p style="color:red; text-align:center; margin:0;">Маркированная продукция отсутствует</p>'
    return render_template('marked.html', message=message)


@bp.route('/action20', methods=['POST'])
def action13():
    if request.method == 'POST':
        product_t = request.form['product_type']
        gln = session['gln']
        email = request.form['email']
        print(request.values)
        statement = diff_user_input(dict(request.values))
        print(statement)
        if statement[0] is False:
            return render_template('area.html', message=statement[1])

        try:
            data = unify_self_signs.document(gln, statement[1], product_t)
            print(data)
            # send_document(SERVICE_EMAIL, email, SERVICE_DIR, gln)
            message = f'<p style="color:green; text-align:center; margin:0;">' \
                      f'Документ успешно отправлен на почту {email}</p> '
            for g in data.keys():
                fur = Furs(gln=data.get(g)[0], gtin=g, kiz=data.get(g)[1],
                           tid=data.get(g)[2], sgtin=data.get(g)[3], sgtin_hex=data.get(g)[4])
                db.session.add(fur)
            db.session.commit()

            return render_template('area.html', message=message)

        except ValueError:
            message = '<p style="color:red; text-align:center; margin:0;">Введены неверные данные</p>'
            return render_template('area.html', message=message)


def diff_user_input(user_input):
    for key in user_input.keys():
        value = [x for x in user_input[key].replace('\r\n', ' ').split(' ') if x != '']
        user_input[key] = tuple(value)
    print(user_input)

    gtin = user_input['gtin']
    kiz = user_input['kiz']
    tid = user_input['tid']

    if len(gtin) != len(kiz) or len(gtin) != len(tid) or len(kiz) != len(gtin) or len(kiz) != len(tid) \
            or len(tid) != len(gtin) or len(tid) != len(kiz):
        message = '<p style="color:red; text-align:center; margin:0;">Количество gtin, kiz и tid не совпадают</p>'
        return False, message

    user_input['kiz'] = list(zip(user_input.get('kiz'), user_input.get('tid')))

    count = 0
    for gtin in user_input.get('gtin'):
        user_input[gtin] = user_input.get('kiz')[count]
        count += 1

    for i in ['gtin', 'kiz', 'tid', 'email', 'product_type']:
        user_input.pop(i, None)
    print(user_input)

    return True, user_input


def send_document(email, gln):
    suffix = '.xml'
    send_mail(send_from=SERVICE_EMAIL, send_to=[email], subject='Маркировка',
              text='во вложении документ для маркировки шуб',
              files=[os.path.join(current_app.instance_path, SERVICE_DIR, gln + suffix)])
