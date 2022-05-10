from flask import Flask
import os

app = Flask(__name__)

from app import views, preprocess, model, utils, functions

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
print(f'ENV is set to: {app.config["ENV"]}')

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'Uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
