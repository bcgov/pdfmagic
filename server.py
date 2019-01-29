import flask
import os
import sys
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './pdf_upload'
ALLOWED_EXTENSIONS = set(['pdf'])


app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET','POST'])
def uploader():
    req = flask.request
    # print('here',file=sys.stderr)
    if req.method == 'POST':
        if 'file[]' not in req.files:
            flask.flash('No file part')
            return flask.redirect(req.url)    
        uploaded_files=req.files.getlist("file[]")
        print("FILES",file=sys.stderr)
        print(uploaded_files,file=sys.stderr)

        upcount = 0

        for _file in uploaded_files:
            if not _file: continue
            if allowed_file(_file.filename):
                filename = secure_filename(_file.filename)
                _file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                upcount += 1
                flask.flash(f'FILES UPLOADED: {upcount}')
            else:
                flask.flash('FILE NOT ALLOWED: {_file.filename}')
    return flask.render_template('pdfmagic.html')
