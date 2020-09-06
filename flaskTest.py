from flask import Flask, render_template, request
from flask import send_file
from werkzeug import secure_filename
import os

PEOPLE_FOLDER = os.path.join('avi')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/', methods=['GET', 'POST'])
def download():
    #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    #return send_from_directory(directory=uploads, filename='rec.avi')
    return send_file('avi/rec.avi', as_attachment=True)

if __name__ == '__main__':
    #서버 실행
    app.run(host = '0.0.0.0')


