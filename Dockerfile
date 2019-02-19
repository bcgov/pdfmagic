FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y uwsgi procps libpcre3 libpcre3-dev&&\
    apt-get install -y poppler-utils tesseract-ocr 

RUN pip install uwsgi pipenv

RUN mkdir -p /pdfmagic
COPY ./src pdfmagic/src
WORKDIR /pdfmagic/src

# pipenv install needs these
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# set up app config
RUN mkdir -p /pdfmagic/uploads /pdfmagic/output
ENV PDFMAGIC_CONFIG /pdfmagic/src/pdfmagic.cfg
ENV WEB_CONCURRENCY 10


EXPOSE 8000

# enter
CMD [ "gunicorn","app:app" ]

