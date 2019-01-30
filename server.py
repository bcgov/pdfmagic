import flask
import os
import sys
from werkzeug.utils import secure_filename
import shutil
from datetime import datetime as dt
import string
import base64

import scrape

UPLOAD_FOLDER = './pdf_upload'
SCRAPE_OUTPUT_FOLDER = './pdf_output'
ALLOWED_EXTENSIONS = set(['pdf'])
SID_SIZE = 30


app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SCRAPE_OUTPUT_FOLDER'] = SCRAPE_OUTPUT_FOLDER

### Returns a boolean value
### whether the filename has an allowed extension or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def batch_scrape(sid):
    scrape.run(os.path.join(app.config['UPLOAD_FOLDER'],sid),batch=True,output=os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid))
    print("DONE",file=sys.stderr)

### zip the output dir of the scraper
def zip_files(sid):
    #tstamp = '-'.join('_'.join(str(dt.now()).split(' ')).split(':')).split('.')[0]
    path = os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid)
    shutil.make_archive(path,'zip',path)

def generate_sid():
    return base64.b64encode(os.urandom(24)).decode().replace('/','0')

@app.route('/',methods=['GET','POST'])
def uploader():
    req = flask.request

    ### POST requests should be file uploads
    if req.method == 'POST':
        #generate session id
        sid = generate_sid()
        flask.session['sid'] = sid

        if 'file[]' not in req.files:
            flask.flash('No file part')
            return flask.redirect(req.url)    
        uploaded_files=req.files.getlist("file[]")
        print("FILES",file=sys.stderr)
        print(uploaded_files,file=sys.stderr)

        upcount = 0

        # process filenames, and save files
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'],sid)
        os.mkdir(upload_folder)
        for _file in uploaded_files:
            if not _file: continue
            if allowed_file(_file.filename):
                filename = secure_filename(_file.filename)
                _file.save(os.path.join(upload_folder,filename))
                upcount += 1
            else:
                flask.flash('FILE NOT ALLOWED: {_file.filename}')
            flask.render_template('pdfmagic.html')
        flask.flash(f'FILES UPLOADED: {upcount}')

        #run the scraper
        batch_scrape(sid)
        zip_files(sid)
    
        return flask.render_template('downloads.html')

    return flask.render_template('pdfmagic.html')

@app.route('/download/')
def download():
    try:
        sid = flask.session['sid']
        return flask.send_file(os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],f'{sid}.zip'))
    except Exception as e:
        flask.flash(str(e))
