function post {
    curl -X POST \
        localhost:5000 \
        -H 'cache-control: no-cache' \
        -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
        -F 'file[]=@/Users/blwakila/pdf_extract/testpdfs/29694 Marshall Road Extension - EAO Assessment Process Memorandum of Agreement copy 3.pdf' \
        -F no_html=''

    echo ''
}

post & post & post & post & post & post & post & post &