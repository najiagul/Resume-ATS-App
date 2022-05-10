from app import app
import logging
import os, shutil
from typing import Union
from flask import Flask, request, render_template, flash, redirect, url_for, session
from app.functions import *
from app.model import *
from transformers import AutoModel, AutoTokenizer 
from werkzeug.utils import secure_filename


@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.errorhandler(500)
def server_error(e: Union[Exception, int]) -> str:
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
    
# MPNet
model = Model(
    model = AutoModel.from_pretrained('./model', local_files_only=True),
        #'sentence-transformers/all-mpnet-base-v2'),
    #, return_token_type_ids=True),
    tokenizer = AutoTokenizer.from_pretrained('./model', local_files_only=True))
        #'sentence-transformers/all-mpnet-base-v2', use_fast = False))
 

@app.route("/upload", methods=['POST'])
def upload() -> str:
    """Process the uploaded files"""
    if request.method == 'POST':

        job_description = request.files.get('job')
        uploaded_files = request.files.getlist('file')

        folder = app.config['UPLOAD_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        for file in uploaded_files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == "":
                flash('No selected file') 
                #return render_template('index.html')
                return redirect(url_for('index'))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Please upload a file with pdf, docx, or txt extension')
                return redirect(url_for('index'))
        
        if job_description.filename == "":
            flash("No job description file uploaded")
            return redirect(url_for('index'))

        if job_description and allowed_file(job_description.filename):
            jobfilename = secure_filename(job_description.filename)
            os.makedirs(f"{app.config['UPLOAD_FOLDER']}/jobs")
            job_description.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/jobs", jobfilename))
        else:
            flash('Please upload a file with pdf, docx, or txt extension')
            return redirect(url_for('index'))
        
        return redirect(url_for('predict'))


@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    return render_template('predict.html') 

@app.route("/resumes", methods = ['GET','POST'])
def sorted_mathing_resumes():
    if request.method == 'POST':
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f))]
        job = (os.listdir(f"{app.config['UPLOAD_FOLDER']}/jobs"))[0]
        dict_result = sort_resumes(model, files, job)
        session['logresumes'] = dict_result
        print(session['logresumes'])
        return redirect(url_for('sorted_mathing_resumes'))
    
    dict_result = session['logresumes']
    return render_template("resumes.html", dict_result = dict_result)
'''

@app.route("/resumes", methods = ['GET'])
def display_resumes():
    try:
        dict_result = session.pop('logresumes')
    except KeyError:
        return render_template("resumes.html")
    return render_template("resumes.html", dict_result = dict_result)
'''

