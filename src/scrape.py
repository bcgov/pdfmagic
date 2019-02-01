import argparse
import subprocess
import glob
import pdf2image
import pytesseract

OUTPUT_FOLDER_DEFAULT = "pdf_output"

#todo: make this more cross-platform?
#todo: make the single-upload experience better

### Extract text from a pdf file using Tesseract OCR
def ocr(pdffile,dirs):
    # convert pdfs to images
    images = pdf2image.convert_from_path(pdffile,output_folder=dirs['img_dir'])
    text = ""
    for image in images:
        # run ocr on image
        text += (pytesseract.image_to_string(image,lang='eng'))
        text += ('\n\n')
    # this is hardcoded but these type of exceptions should be loaded in a config file
    if 'Public Comment Form' in text:
        subprocess.run(['mv',pdffile,dirs['forms']])
    else:
        # save text file
        txtfile = dirs['ocr_dir']+'/'+((pdffile.split('/')[-1]).split('.')[0] + '.txt')
        with open(txtfile,'w') as txt:
            txt.write(text)

### Scrape text from a pdf using pdftotext from Poppler
def scrape(pdffile,dirs):
    if pdffile[-4:] != '.pdf': return
    
    # "good" files are text pdfs that don't need OCR
    good = False
    subprocess.run(['pdftotext',pdffile])
    print(pdffile)
    txtfile = ('.'.join(pdffile.split('.')[:-1]) + '.txt')
    print(txtfile)

    # check if the .txt file is "good" (not empty)
    with open(txtfile,'r') as txt:
        if txt.read().strip():
            good = True
    if good: 
        # save .txt of good file
        subprocess.run(['mv',txtfile,dirs['scraped']])
    else:
        # put bad pdfs in a special dir and delete the empty .txt
        subprocess.run(['cp',pdffile,dirs['noscrape']])
        subprocess.run(['rm',txtfile])

### Return list of .pdf files in a target dir
def get_pdfs(target):
    gl = glob.glob(target + '/*.pdf')
    print(gl)
    return gl

### Return arg parser object
def init_argparser():
    parser = argparse.ArgumentParser(description="Scrapes scrapable pdfs and OCRs those that are not, separating the two.")
    parser.add_argument('target')
    parser.add_argument('-o','--output')
    parser.add_argument('-b','--batch',action='store_true')
    return parser

### Return dict with all output subdirs
def init_dirs(output_dir):
    output_dir = output_dir.strip()
    dirs = {}
    dirs['scraped'] = output_dir + '/scraped'
    dirs['noscrape'] = output_dir + '/noscrape'
    dirs['ocr_dir'] = output_dir + '/ocr'
    dirs['img_dir'] = output_dir + '/img'
    dirs['forms'] = output_dir + '/forms'

    # make output dir and subdirs
    subprocess.run(['mkdir',output_dir])
    for dir in dirs.values():
        subprocess.run(['mkdir',dir])
    return dirs

### Shouldn't really be called directly
def start(args):
    output = args.output.strip('/') if args.output else OUTPUT_FOLDER_DEFAULT
    dirs = init_dirs(output)

    if args.batch:
        for pdf in get_pdfs(args.target):
            if pdf: scrape(pdf,dirs)
    else:
        scrape(args.target,dirs)


    for pdf in get_pdfs(dirs['noscrape']):
            ocr(pdf,dirs) 

    
    
    #remove temp dirs
    subprocess.run(['rm','-r',dirs['noscrape']])
    subprocess.run(['rm','-r',dirs['img_dir']])

### This function can be called externally, 
### its parameters create args equivalent to command-line
def run(target,batch=False,output=OUTPUT_FOLDER_DEFAULT):
    parser = init_argparser()
    if batch: 
        args = parser.parse_args([target,'-b','-o '+output])
    else:
        args = parser.parse_args([target,'-o '+output])
    
    start(args)

if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    # print(args)
    start(args)
    