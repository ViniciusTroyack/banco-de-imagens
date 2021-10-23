import os

FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)