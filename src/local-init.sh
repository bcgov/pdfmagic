dir="$1"

upload_dir="$dir/pdf_upload"
output_dir="$dir/pdf_output/"
celery_data="$dir/celery_data"
celery_processed="$dir/celery_processed"

echo "DEBUG = False" > local.cfg
echo "UPLOAD_FOLDER = '$upload_dir'" >> local.cfg
echo "SCRAPE_OUTPUT_FOLDER = '$output_dir'" >> local.cfg
echo "CELERY_PATH_DATA = '$celery_data'" >> local.cfg
echo "CELERY_PATH_PROCESSED = '$celery_processed'" >> local.cfg

cd "$dir"
mkdir "$upload_dir" "$output_dir" "$celery_data" "$celery_processed"