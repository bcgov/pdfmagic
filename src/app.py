import flask
import os
import sys
from werkzeug.utils import secure_filename
import shutil
from datetime import datetime as dt
import string
import base64
import glob

import scrape

ALLOWED_EXTENSIONS = set(['pdf'])
SID_SIZE = 30


app = flask.Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']


app.config.from_envvar('PDFMAGIC_CONFIG')

### Returns a boolean value
### whether the filename has an allowed extension or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

### todo: create a workflow for single upload
### Run the scraper on a folder
### sid is used to uniquely identify this session's files
def batch_scrape(sid):
    scrape.run(os.path.join(app.config['UPLOAD_FOLDER'],sid),batch=True,output=os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid))
    zip_files(sid)
    print("BATCH DONE",file=sys.stderr)

def single_scrape(sid):
    scrape.run(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'],sid,flask.session['filename'])),batch=False,output=os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid))
    print("DONE",file=sys.stderr)

### zip the output dir of the scraper
### sid is used to uniquely identify this session's files
def zip_files(sid):
    #tstamp = '-'.join('_'.join(str(dt.now()).split(' ')).split(':')).split('.')[0]
    path = os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid)
    shutil.make_archive(path,'zip',path)

### Generate a random session id string
def generate_sid():
    return base64.b64encode(os.urandom(24)).decode().replace('/','0')

### Save a file to disk if it matches allowed filetypes
### return false if file not allowed, true otherwise
def save_file(_file,upload_folder):
    if allowed_file(_file.filename):
        filename = secure_filename(_file.filename)
        filepath = os.path.join(upload_folder,filename)
        _file.save(filepath)
        if not flask.session['batch']: flask.session['filename'] = filename
        return True
    else:
        flask.flash('FILE NOT ALLOWED: {_file.filename}')
        return False
    

### Main route, displays upload page on GET
### Handles .pdf upload on POST
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

        # is a batch job if there is more than one file
        flask.session['batch'] = len(uploaded_files) > 1
        

        # process filenames, and save files
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'],sid)
        os.mkdir(upload_folder)
        for _file in uploaded_files:
            if not _file: continue
            save_file(_file,upload_folder)
            flask.render_template('pdfmagic.html')

        #run the scraper
        if flask.session['batch']:
            batch_scrape(sid)
        else:
            single_scrape(sid)
        
        if req.form['no_html']:
            return req.base_url + '/download/'
            
        return flask.render_template('downloads.html')

    return flask.render_template('pdfmagic.html')

### User can download output zip with a GET
@app.route('/download/')
def download():
    try:
        sid = flask.session['sid']
        tstamp = '-'.join('_'.join(str(dt.now()).split(' ')).split(':')).split('.')[0]
        if flask.session['batch']:
            return flask.send_file(os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid+'.zip'),as_attachment=True,attachment_filename='pdfmagic-{}.zip'.format(tstamp))
        else:
            try:
                txtfile = glob.glob(os.path.join(app.config['SCRAPE_OUTPUT_FOLDER'],sid,'*','*.txt'))[0]
                return flask.send_file(txtfile,as_attachment=True,attachment_filename=flask.session['filename'][:-3]+'.txt')
            except Exception as e:
                return str(e)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(
        debug=False,
        port=8080
    )