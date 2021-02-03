from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import tensorflow as tf
from flask_bcrypt import Bcrypt
from datetime import datetime
# from prometheus_flask_exporter import PrometheusMetrics
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd

import os
from io import StringIO
from werkzeug.utils import secure_filename
from flask import send_from_directory
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'C:/uploads'
app = Flask(__name__)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)
""" cors = CORS(app, resources={r"*": {"origins": "*"}}) """
cors = CORS(app, resources={
    r"/api/*": {
        "origins": "*"
    }
})


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


""" Read content of file """
@app.route('/file/read', methods=['GET'])
def get_file():
    with open('data.csv', 'r') as f:
        data = f.read()
        print(data)
    return data

@app.route('/file/openfilecsv', methods=['GET'])
def get_openfilecsv():
    # df = pd.read_csv(StringIO('D:\emploi\projet\data.csv'))
    df = pd.read_csv('D:/emploi/projet/data.csv')
    print(df)
    dff = df.to_json()
    return jsonify(dff)


# Enregistrer dans le path 'C:/uploads'/cv-nourhene.pdf
@app.route("/upload", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      return file_path

# Enregistrer ficher dans le meme repertoire de projet 
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

# Enregistrer ficher dans 'C:/uploads'
@app.route('/file-upload', methods=['POST'])
def upload_filee():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp




""" Display list the file in this folder """
""" @app.route('/file/readpath', methods=['GET'])
def get_filee():
    path = r"D:\emploi\projet"
    directories = os.listdir( path )
    for file in directories:
        
    return file """

""" Display list the file in this folder Open a file """
@app.route('/file/openfile', methods=['GET'])
def get_openfile():
    path = r"D:\emploi\projet"
    
    for files in os.listdir(path):
        if os.path.isdir(os.path.join(path, files)):
            print(files)
    return files


if __name__ == "__main__":
    app.run(debug=True, port=5002)