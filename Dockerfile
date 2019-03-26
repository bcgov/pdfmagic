FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y procps libpcre3 libpcre3-dev&&\
    apt-get install -y poppler-utils tesseract-ocr 

RUN pip install pipenv

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
RUN mkdir -p /pdfmagic/celery/data /pdfmagic/celery/processed
RUN chgrp -R 0 /pdfmagic/uploads && chmod -R g+rwx /pdfmagic/uploads
RUN chgrp -R 0 /pdfmagic/output && chmod -R g+rwx /pdfmagic/output
RUN chgrp -R 0 /pdfmagic/celery && chmod -R g+rwx /pdfmagic/celery


ENV PDFMAGIC_CONFIG /pdfmagic/src/pdfmagic.cfg
ENV WEB_CONCURRENCY 10


EXPOSE 5000

# enter
CMD [ "gunicorn","-b","0.0.0.0:5000","-t","60","app:app" ]

