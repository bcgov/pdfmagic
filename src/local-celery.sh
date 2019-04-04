export PDFMAGIC_CONFIG=local.cfg
export FLASK_SECRET_KEY=1234567890

celery worker =A app.celery --loglevel=info