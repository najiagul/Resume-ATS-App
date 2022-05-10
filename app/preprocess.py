import re
import textract
import os
from app import app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}


'''def read_pdf(pdf_path):
  text = textract.process(pdf_path)
  # decode text 
  text = text.decode("utf-8")

  # remove emails  
  pattern1 = '\S*@\S*\s?'
  text = re.sub(pattern1, ' ', text)

  # remove special characters
  pattern2 = r"[^.,'a-zA-Z\n\.]"
  text = re.sub(pattern2, ' ', text)

  # remove white spaces and lines
  pattern3 = '\s+'
  text = re.sub(pattern3, ' ', text)
  return text'''
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_docx_pdf(filename):
    text = textract.process(filename)
    # decode text 
    text = text.decode("utf-8")

    # remove emails  
    pattern1 = '\S*@\S*\s?'
    text = re.sub(pattern1, ' ', text)

    # remove special characters
    pattern2 = r"[^.,'a-zA-Z\n\.]"
    text = re.sub(pattern2, ' ', text)

    # remove white spaces and lines
    pattern3 = '\s+'
    text = re.sub(pattern3, ' ', text)
    return text

def read_txt(filename):
  with open(filename, 'rb') as f:
    text = f.read().decode(errors='replace')

  # remove white spaces and lines
  pattern3 = '\s+'
  text = re.sub(pattern3, ' ', text)
  return text


def preprocess(filename):
  if filename.endswith("txt"):
      text = read_txt(filename)
  else:
      text = read_docx_pdf(filename)
  return text

def batch_preprocess(files = None, job_file = None):
  'Returns a dictionary object and a string containing resume text and job text respectively'
  
  # read resume paths and preprocess
  resumes = {}
  for file in files:
    processed = preprocess(os.path.join(app.config['UPLOAD_FOLDER'], file))
    if processed is not None:
      resumes[file] = processed

  # read job path and get a string
  job_text = preprocess(os.path.join(f"{app.config['UPLOAD_FOLDER']}/jobs", job_file))
  if job_text is not None:
     return resumes, job_text
  else:
    print('Error reading job file')
    return
    
 