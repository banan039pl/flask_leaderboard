import json
import pathlib


def create_folder(dirr):
    """Create directory given directory. Parent directories are created as well if don't exist. If directory already exists then function does nothing"""
    pathlib.Path(dirr).mkdir(parents=True, exist_ok=True)

def file_to_dict(file):
    """Dump json file to dict"""
    try:
        with open(file) as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        print(f'File {file} is not a valid json file. Returning empty dict')
        return {}
    except FileNotFoundError:
        print(f'File {file} does not exist. Returning empty dict')
        return {}

