import os
import pathlib
import pandas as pd
from sklearn.metrics import mean_squared_error
from files_lib import SHA256
from Models import Results, Submission


def create_folder(PATH):
    """Create directory for given PATH. Parent directories are created as well if don't exist. If directory already exists then function does nothing"""
    pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)

class Scorer():
    """Class for calculating score. TODO: make it a function"""
    def __init__(self, public_path = './master_key/public_key.csv', 
                private_path = './master_key/private_key.csv', metric=mean_squared_error):
        self.public_path = public_path
        self.private_path = private_path
        self.metric = metric

        self.df_public_key = pd.read_csv(self.public_path)
        self.df_private_key = pd.read_csv(self.private_path)
        
    def calculate_score(self, ctf_flag, submission_path, subject_type, task, user_id,submission_type='public'):
        """Calculate score for submission. TODO: custom scoring"""
        # check if task was already solved by user
        is_solved = Submission.query.filter_by(
                                             user_id=user_id,
                                             submission_type=submission_type,
                                             subject_type=subject_type,
                                             task=task,
                                             submission_status='SUBMISSION SUCCESS'
                                            ).first()
        if is_solved is None: # Task was not solved yet
            ctf_flag_hashed = SHA256(ctf_flag)
            # Compare hashed flag to the hashed flag in the database
            hashed_flag = Results.query.filter_by(
                task=task,
                subject_type=subject_type,
                flag=ctf_flag_hashed
            ).first()
            # If flag is incorrect
            if hashed_flag is None:
                return "WRONG_ANSWER", 0.0
            else:
                return "SUBMISSION SUCCESS", hashed_flag.points
        else:
            submission_status = "SUBMISSION ALREADY SOLVED\n{" + subject_type.upper() + \
                                "}{TASK: " + str(task) + "}" + \
                                "\n\nPLEASE SOLVE ANOTHER TASK!"
            return submission_status, None
