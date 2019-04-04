export PDFMAGIC_CONFIG=local.cfg
export FLASK_SECRET_KEY=1234567890

gunicorn -b localhost:5000 -t 60 app:app