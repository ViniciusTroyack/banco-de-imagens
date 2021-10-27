from flask import Flask, send_from_directory, request, jsonify
import os
from .kenzie.image import utils

app = Flask(__name__)

MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH'))
FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.post("/upload/<filename>")
def post_file(filename):
    
    DIR = utils.verify_dir(filename)

    if not utils.is_allowed_file(filename):
        return{"message": "Unsupported Media Type"}, 415

    if filename in os.listdir(DIR):
        return{"message": "File already exists "}, 409

    with open(f"{DIR}/{filename}", "wb") as f:
        f.write(request.data)
        
    return {"message": "Upload successful"}, 201


@app.get('/files')
def list_files():
    
    list = utils.files_list()
    return jsonify(list), 200


@app.get('/files/<extension>')
def list_files_by_extension(extension):

    if not extension in os.listdir(FILES_DIRECTORY):
        return{"message": "File not Fount"}, 404

    list = utils.files_list(extension)
    return jsonify(list), 200


@app.get("/download/<file_name>")
def download(file_name):
    extension_path = utils.find_extension(file_name)

    if not extension_path in os.listdir(FILES_DIRECTORY):
        return{"message": "File not Fount"}, 404

    if not file_name in os.listdir(f'{FILES_DIRECTORY}{extension_path}'):
         return{"message": "File not Fount"}, 404

    return send_from_directory(directory="../files", path=f"{extension_path}/{file_name}", as_attachment=True), 200


@app.get('/download-zip')
def download_zip():

    file_extension = request.args.get('file_extension')
    compression_ratio = request.args.get('compression_ratio')

    if not file_extension in os.listdir(FILES_DIRECTORY):
        return{"message": "File not Fount"}, 404

    return os.system(f"zip -{compression_ratio} -r /temp/{file_extension}.zip {FILES_DIRECTORY}{file_extension}"), 200

