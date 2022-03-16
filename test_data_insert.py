from Models import Results
from files_lib import SHA256, file_to_dict
from main import db, User, Submission

def test_user_submission():
    u = User(username="karje1", password=SHA256("karje1"), faction='', apikey='')
    db.session.add(u)
    db.session.commit()

    s = Submission(user_id=1, score=0.5, submission_type='public')
    db.session.add(s)
    db.session.commit()


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
    data = file_to_dict('config_local.json')
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


insert_tasks_from_json()