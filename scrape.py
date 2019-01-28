import argparse
import subprocess
import glob
import pdf2image
import pytesseract

OUTPUT_FOLDER_DEFAULT = "./pdf_output"

def ocr(pdffile,ocr_dir,img_dir):
    images = pdf2image.convert_from_path(pdffile,output_folder=img_dir)
    text = ""
    for image in images:
        text += (pytesseract.image_to_string(image,lang='eng'))
        text += ('\n\n')
    txtfile = ocr_dir+'/'+((pdffile.split('/')[-1]).split('.')[0] + '.txt')
    with open(txtfile,'w') as txt:
        txt.write(text)

def scrape(pdffile,scraped,noscrape):
    if pdffile[-4:] != '.pdf': return
    good = False
    subprocess.run(['pdftotext',pdffile])
    print(pdffile)
    txtfile = ('.'.join(pdffile.split('.')[:-1]) + '.txt')
    print(txtfile)
    with open(txtfile,'r') as txt:
        if txt.read().strip():
            good = True
    if good: 
        subprocess.run(['mv',txtfile,scraped])
    else:
        subprocess.run(['cp',pdffile,noscrape])
        subprocess.run(['rm',txtfile])

def get_pdfs(target):
    gl = glob.glob(target + '/*.pdf')
    print(gl)
    return gl

def init_argparser():
    parser = argparse.ArgumentParser(description="Scrapes scrapable pdfs and OCRs those that are not, separating the two.")
    parser.add_argument('target')
    parser.add_argument('-o')
    parser.add_argument('-r',action='store_true')
    return parser

def init_dirs(output_dir):
    scraped = output_dir + '/scraped'
    noscrape = output_dir + '/noscrape'
    ocr_dir = output_dir + '/ocr'
    img_dir = output_dir + '/img'
    subprocess.run(['mkdir',output_dir])
    subprocess.run(['mkdir',scraped])
    subprocess.run(['mkdir',noscrape])
    subprocess.run(['mkdir',ocr_dir])
    subprocess.run(['mkdir',img_dir])
    return scraped,noscrape,ocr_dir,img_dir

if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    print(args)
    output = args.o.strip('/') if args.o else OUTPUT_FOLDER_DEFAULT
    scraped,noscrape,ocr_dir,img_dir = init_dirs(output)

    if args.r:
        for pdf in get_pdfs(args.target):
            if pdf: scrape(pdf,scraped,noscrape)
        else:
            scrape(args.target,scraped,noscrape)

    for pdf in get_pdfs(noscrape):
        ocr(pdf,ocr_dir,img_dir)