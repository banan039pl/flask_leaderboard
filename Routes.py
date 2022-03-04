from flask import request, url_for, render_template
from werkzeug.utils import redirect

from Models import User
from files_lib import SHA256
from forms import RegisterForm


def register_route(db):
    registration_status = request.args.get("registration_status", "")
    reg_form = RegisterForm()

    if request.method == 'POST':
        ### REGISTRATION
        if reg_form.validate_on_submit():
            user = User.query.filter_by(username=reg_form.username.data).first()
            print(user)
            if user is None:  # only when user is not registered then proceed
                print("HALOOO")
                u = User(username=reg_form.username.data, password=SHA256(reg_form.password.data),
                         faction=reg_form.faction.data)
                db.session.add(u)
                db.session.commit()
                # flash('Congratulations, you are now a registered user!')
                registration_status = f"Welcome {reg_form.username.data}, Please Login at HOME page"
                return redirect(url_for('register_page', registration_status=registration_status))
            else:
                registration_status = "USER NAME ALREADY USED"
                return redirect(url_for('register_page', registration_status=registration_status))
        else:
            registration_status = "ERROR VALIDATION"
            print("ANEH")
            return redirect(url_for('register_page', registration_status=registration_status))

    if request.method == 'GET':
        return render_template('register.html', reg_form=reg_form, registration_status=registration_status)

def Logging_in(login_form, login_user):
    print(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
    user = User.query.filter_by(username=login_form.username.data).first()
    if user is None:  # USER is not registered
        login_status = "User is not registered / Password does not match"
        return redirect(url_for('home_page', login_status=login_status))
    elif user.check_password(login_form.password.data):  # Password True
        print('True pass')
        login_status = ""
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('home_page', login_status=login_status))
    else:  # WRONG PASSWORD
        print('WRONG PASS')
        login_status = "User is not registered / Password does not match"
        return redirect(url_for('home_page', login_status=login_status))
    login_status = ""
    login_user(user, remember=login_form.remember_me.data)
    return redirect(url_for('home_page', login_status=login_status))