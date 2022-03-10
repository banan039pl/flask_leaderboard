from flask import Flask, url_for
from flask_admin import AdminIndexView
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect

from files_lib import SHA256
import pandas as pd

app = Flask(__name__)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    """Table for users, their factions and hashed passwords"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128)) ## Too lazy to make it hash
    faction = db.Column(db.String(64))

    def __repr__(self):
        return self.username

    def check_password(self, password): ## Too lazy to make it hash
        return SHA256(password) == self.password

class Submission(db.Model):
    """"Table which stores users submissions and scores"""
    __tablename__ = "submission"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.now)
    submission_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    score = db.Column(db.Float)
    subject_type = db.Column(db.String(64))
    task = db.Column(db.String(64))
    submission_status = db.Column(db.String(64))


    def __repr__(self):
        return f'<User ID {self.user_id} score {self.score}>'

class Results(db.Model):
    """Table which stores hashed flags for CTF tasks for each subject_type"""
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    subject_type = db.Column(db.String(64))
    task = db.Column(db.String(64))
    flag = db.Column(db.String(64))

    def __repr__(self):
        return f'<subject_type {self.subject_type} task {self.task}>'

# Admin
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

class UserView(ModelView):
    column_list = (User.id, 'username','password')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

class SubmissionView(ModelView):
    column_list = (Submission.id, 'submission_type', 'user_id', 'user',  'timestamp', 'score', 'subject_type', 'task', 'submission_status')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

class ResultsView(ModelView):
    column_list = (Results.id, 'subject_type', 'task', 'flag')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username == 'admin'
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home_page'))

def get_leaderboard(greater_better, limit, submission_type = 'public'):
    """Query the database for submissions results, then return it in a form of a dataframe"""
    if greater_better:
        score_agg = "SUM"
        #score_agg = "MAX"
        score_sorting = "DESC"
    else:
        score_agg = "MIN"
        score_sorting = "ASC"
    #{score_agg}(submission.score) as score,
    query = f"""
            SELECT
            user.username, 
            user.faction,
            SUM(submission.score) as score,
            count(submission.id) as total_submission,
            max(timestamp) as last_sub
            FROM submission 
            LEFT JOIN user 
            ON user.id = submission.user_id
            WHERE submission_type = '{submission_type}'
            GROUP BY 1 
            ORDER BY 2 {score_sorting}, 4
            LIMIT {limit}
            """
    df = pd.read_sql(query, db.session.bind)
    return df

def get_leaderboard_factions(limit=100):
    """Query the database for scores earned by each faction"""
    query = f"""
            SELECT DISTINCT 
            user.faction,
            SUM(submission.score) as score
            FROM submission
            LEFT JOIN user 
            ON user.id = submission.user_id
            ORDER BY score DESC
            LIMIT {str(limit)}
            """
    df = pd.read_sql(query, db.session.bind)
    return df

def validate_tables(db):
    """Check if the database has proper tables and columns"""
    table_name = 'results'
    t_exists = db.execute(f'SELECT * FROM {table_name}')
