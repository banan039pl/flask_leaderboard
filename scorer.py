import os
import pathlib

import pandas as pd

from sklearn.metrics import mean_squared_error

from files_lib import SHA256
from Models import Results


def create_folder(dirr):
    """Create directory given directory. Parent directories are created as well if don't exist. If directory already exists then function does nothing"""
    pathlib.Path(dirr).mkdir(parents=True, exist_ok=True)

class Scorer():
    def __init__(self, public_path = './master_key/public_key.csv', 
                private_path = './master_key/private_key.csv', metric = mean_squared_error):
        self.public_path = public_path
        self.private_path = private_path
        self.metric = metric

        self.df_public_key = pd.read_csv(self.public_path)
        self.df_private_key = pd.read_csv(self.private_path)
        
    def calculate_score(self, ctf_flag, submission_path, subject_type, task, submission_type = 'public'):
        #return ("SUBMISSION SUCCESS", 1.0)
        # Save the flag locally
        with open(submission_path, 'w') as f:
            f.write(ctf_flag.strip())
        ctf_flag_hashed = SHA256(ctf_flag.strip())
        hashed_flag = Results.query.filter_by(task=task,subject_type=subject_type,flag=ctf_flag_hashed).first()
        if hashed_flag is None:
            return ("WRONG_ANSWER", 0.0)
        else:
            return ("SUBMISSION SUCCESS", 1.0)
