# pdfmagic
A common service deployable project to handle conversion of PDF documents to text

## Developing Locally
Unfortunately this probably will not run on windows right now.

Dependencies:
(these should all be in your PATH)

Brew and Apt packages listed for convenience, follow the links for installation instructions on your system.

 - Python 3.7 & Pip

 - [Poppler](https://poppler.freedesktop.org/)
 
 `brew install poppler` OR `sudo apt install poppler-utils`
 
 - [Tesseract](https://github.com/tesseract-ocr/tesseract)
 
 `brew install tesseract` OR `sudo apt install tesseract-ocr`
 - [pipenv](https://pipenv.readthedocs.io/en/latest/)
 
 `pip install pipenv`
 
Setup instructions:
 
Install python dependencies
    
    cd src
    pipenv install
    
Run celery worker

    celery worker -A app.celery --loglevel=info
    
Run app

    ./local.sh
