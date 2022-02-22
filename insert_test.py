from files_lib import SHA256
from main import db, User, Submission

u = User(username="karje1", password = SHA256("karje1"))
db.session.add(u)
db.session.commit()

s = Submission(user_id=1 , score=0.5, submission_type = 'public')
db.session.add(s)
db.session.commit()