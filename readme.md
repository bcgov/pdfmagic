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
    
Make a data directory and run the one-time init script
(only do this the first time setting up, the directory can be named anything)

    mkdir ~/pdfmagic_data
    ./local-init.sh ~/pdfmagic_data
    
Run celery worker

    pipenv shell
    ./local-celery.sh
    
Run app in another terminal
    
    pipenv shell
    ./local-flask.sh

## Usage

For testing the API I recommend using [Postman](https://www.getpostman.com/)
There are a few API endpoints available currently:

### POST

`/extract-keywords/` or `/upload/`

Both of these expect a file in the request form-data with key `file[]` 

`/extract-keywords/` also accepts comma separated case-insensitive keywords in the request form-data with key `keywords`. If the optional `snippets` parameter is set to `true` then it will attempt to return small snippets of text relevant to keywords. This feature does not work well

eg:

    curl -X POST \
      http://localhost:5000/extract-keywords/?snippets=false \
      -H 'cache-control: no-cache' \
      -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
      -F 'file[]=@/path/to/file.pdf' \
      -F 'keywords=Just, Some, keywords'
 
 ### GET
 
 `/retrieve-keywords/` : returns json with the counts of the keywords
 
 `/download/` : returns txt of the pdf
 
 Both of these can be used after a `/extract-keywords/` but only `/download/` should be used after an `/upload/`
 
 There is a cookie returned from the POST which needs to be given in order to retrieve any data from the server.
 
