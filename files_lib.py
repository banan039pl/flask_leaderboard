import json
import pathlib
import hashlib


def create_folder(dirr: str):
    """Create directory given directory. Parent directories are created as well if don't exist. If directory already exists then function does nothing"""
    pathlib.Path(dirr).mkdir(parents=True, exist_ok=True)

def file_to_dict(file: str):
    """Dump json file to dictionary"""
    try:
        with open(file) as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        print(f'File {file} is not a valid json file. Returning empty dict')
        return {}
    except FileNotFoundError:
        print(f'File {file} does not exist. Returning empty dict')
        return {}

def get_local_config_data(section='',file='config_local.json'):
    data = file_to_dict(file)
    if section:
        return data[section]
    else:
        return data

def SHA256(s: str):
    """Convert string to hex sha256 hash in uppercase string format"""
    data = str(s).encode()
    return hashlib.sha256(data).hexdigest().upper()
