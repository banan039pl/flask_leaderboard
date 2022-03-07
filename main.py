import numpy as np 
import pandas as pd
import os
import datetime as dt

from flask import Flask,render_template,url_for,request,g, flash, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_user, logout_user, UserMixin
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView

from sklearn.metrics import mean_absolute_error

import Models
from Routes import register_route, Logging_in
from files_lib import SHA256
from forms import LoginForm, RegisterForm
from config import Config
from scorer import Scorer, create_folder
from Models import User, Results, Submission, get_leaderboard
# PARAMETER

## Leaderboard parameter
limit_lb = 100 # Number of user showed at leaderboard table
greater_better = True # True if lowest score is the best; False if greatest score is the best
metric = mean_absolute_error #change the metric using sklearn function
scorer = Scorer(public_path='./master_key/public_key.csv',
                private_path='./master_key/private_key.csv',
                metric=metric) #change the metric using sklearn function

## Upload parameter
UPLOAD_FOLDER = 'submissions'
ALLOWED_EXTENSIONS = {'csv', 'txt'} # only accept csv files

## FLASK configuration
app = Models.app
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # 10 Megabytes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'my'
app.config.from_object(Config)

## Database configuration
db = Models.db
db.app = app
migrate = Migrate(app, db)
login = LoginManager(app)

# Database Model
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

db.create_all()
admin = Admin(app, index_view=Models.MyAdminIndexView())
admin.add_view(Models.UserView(User, db.session))
admin.add_view(Models.SubmissionView(Submission, db.session))
admin.add_view(Models.ResultsView(Results, db.session))
# Leader Board


# Route
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register_route(db)

@app.route('/logout')
def logout():
    logout_user()
    print("log out success")
    return redirect(url_for('home_page'))

def allowed_file(filename):
    # checks if extension in filename is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home_page():
    subject_type = request.form.get("subject_type", "misc")
    task = request.form.get("task", "")
    login_form = LoginForm()
    login_status = request.args.get("login_status", "")
    submission_status = request.args.get("submission_status", "")


    leaderboard = get_leaderboard(greater_better=greater_better, limit=limit_lb, submission_type='public')
    leaderboard_private = get_leaderboard(greater_better=greater_better, limit=limit_lb, submission_type='private')

    if request.method == 'POST': # If upload file / Login
        ### LOGIN 
        if login_form.validate_on_submit():
            return Logging_in(login_form, login_user)
        ### UPLOAD FILE
        if 'ctf_flag' in request.form.keys() and current_user.is_authenticated:
            print('Uploading CTF')
            ctf_flag = request.form['ctf_flag']
            if not ctf_flag:
                return redirect(url_for('home_page', submission_status='SUBMISSION_MUST_NOT_BE_EMPTY!'))
            dirname = os.path.join(app.config['UPLOAD_FOLDER'], subject_type, task, str(current_user.id))
            fullPath = os.path.join(dirname, 'test.txt')
            create_folder(dirname)
            # If submission exists do...
            if os.path.exists(fullPath):
                pass
                #return redirect(url_for('home_page', submission_status='SUBMISSION_ALREADY_EXISTS!'))
            print(fullPath, ctf_flag)
            submission_type = request.form.get('submission_type', "public")
            result = scorer.calculate_score(ctf_flag=ctf_flag,
                                            submission_path=fullPath,
                                            subject_type=subject_type,
                                            task=task,
                                            submission_type=submission_type,
                                            user_id=current_user.id)
            submission_status = result[0]
            if submission_status == "SUBMISSION SUCCESS":
                score = round(result[1], 3)
                s = Submission(user_id=current_user.id,
                               score=score,
                               submission_type=submission_type,
                               subject_type=subject_type,
                               task=task,
                               submission_status=submission_status)
                db.session.add(s)
                db.session.commit()
                print(f"submitted {score}")
                submission_status =  f"SUBMISSION SUCCESS | Score: {round(score,3)}"
            elif submission_status=="WRONG_ANSWER":
                submission_status = f"WRONG ANSWER | SCORE: 0.0"
            return redirect(url_for('home_page', submission_status=submission_status))
            
    return render_template('index.html', 
                        leaderboard=leaderboard,
                        leaderboard_private=leaderboard_private,
                        login_form=login_form, 
                        login_status=login_status,
                        submission_status=submission_status
                        )
def add_test_flag():
    r = Results(subject_type='Forensic',
                task='Zad1',
                flag=SHA256('CTF'))
    db.session.add(r)
    db.session.commit()

if __name__ == '__main__':
    add_test_flag()
    app.debug = True
    app.run(host='0.0.0.0',port=5005)