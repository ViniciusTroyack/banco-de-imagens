import os
from flask.helpers import safe_join

def find_extension(file):
    return file.split('.')[-1]

def verify_dir(file):
    
    FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
    dir = find_extension(file)
    NEW_DIRECTORY = f'{FILES_DIRECTORY}{dir}'
    
    if not os.path.isdir(NEW_DIRECTORY):
        os.mkdir(NEW_DIRECTORY)

    return NEW_DIRECTORY

def is_allowed_file(file):
    
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')
    extension = find_extension(file)
    return extension in ALLOWED_EXTENSIONS


def files_list(extension=False):
    FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
    list_all = []
    
    if extension:
        LIST_DIRECTORY = f'{FILES_DIRECTORY}{extension}'
        _, _, files_list = list(os.walk(LIST_DIRECTORY))[0]
        list_all.extend(files_list)
        return list_all
    
    for folder in os.listdir(FILES_DIRECTORY):
        LIST_DIRECTORY = f'{FILES_DIRECTORY}{folder}'
        _, _, files_list = list(os.walk(LIST_DIRECTORY))[0]
        list_all.extend(files_list)

    return list_all

def save_file(file):
    path_to_save = verify_dir(file.filename)

    path = safe_join(path_to_save, file.filename)
    file.save(path)

    return file.filename

