import pandas as pd
from Models import User
from Models import Results
from files_lib import SHA256, file_to_dict
from main import db, Submission


def add_test_flag():
    r = Results(subject_type='Forensic',
                task='Zad1',
                flag=SHA256('CTF'))
    db.session.add(r)
    r = Results(subject_type='Forensic',
                task='Zad2',
                flag=SHA256('CTF2'))
    db.session.add(r)
    db.session.commit()


def insert_tasks_from_json():
    """"""
    data = file_to_dict(r'D:\PythonProjects\config_local.json')
    tasks = data['tasks']

    for subject_type in data['tasks']:
        for task in data['tasks'][subject_type]:
            HASH = SHA256(data['tasks'][subject_type][task])
            the_task = Results.query.filter_by(
                subject_type=subject_type,
                task=task,
                flag=HASH
            ).first()
            if the_task is None:
                print(f'Task {task} for subject type {subject_type} does not exists, inserting to database')
                t = Results(
                    subject_type=subject_type,
                    task=task,
                    flag=HASH,
                    points=5
                )
                db.session.add(t)
                db.session.commit()
            else:
                print(f'Task {task} for subject type {subject_type} already exists, skipping')


def add_users():
    """add users from csv file"""
    df = pd.read_csv(r'D:\PythonProjects\Kwiatki.csv',sep=';')
    #print(df.head())
    #print(User.query.delete())
    for i, row in df.iterrows():
        user = User.query.filter_by(username=row.username).first()
        if user is None:
            print(f'User {row.username} does not exist, creating')
            u = User(
                username=row.username,
                password=SHA256(row.password),
                faction=row.faction,
                apikey=row.apikey
            )
            db.session.add(u)
            db.session.commit()
        else:
            print(f'User {row.username} already exists, skipping')


def add_test_users():
    for i in range(1,6):
        username = 'test_user_{}'.format(i)
        password = 'test_user_PASS'.format(i)
        user = User.query.filter_by(username=username).first()
        if user is None:
            print(f'User {username} does not exist, creating')
            u = User(
                username=username,
                password=SHA256(password),
                faction='STOKROTKA',
                apikey='no apikey for test users'
            )
            db.session.add(u)
            db.session.commit()
        else:
            print(f'User {username} already exists, skipping')


def remove_test_users(db):
    for i in range(1, 6):
        username = 'test_user_{}'.format(i)
        user = User.query.filter_by(username=username).first()
        if user is None:
            print(f'Test user {username} does not exist, skipping')
        else:
            print(f'Test user {username} exist, removing from database')
            u = User.query.filter_by(username=username).delete()
            db.session.commit()


add_test_users()