import argparse
import subprocess
import glob
import pdf2image
import pytesseract

OUTPUT_FOLDER_DEFAULT = "pdf_output"

def ocr(pdffile,dirs):
    images = pdf2image.convert_from_path(pdffile,output_folder=dirs['img_dir'])
    text = ""
    for image in images:
        text += (pytesseract.image_to_string(image,lang='eng'))
        text += ('\n\n')

    if 'Public Comment Form' in text:
        subprocess.run(['mv',pdffile,dirs['forms']])
    else:
        txtfile = dirs['ocr_dir']+'/'+((pdffile.split('/')[-1]).split('.')[0] + '.txt')
        with open(txtfile,'w') as txt:
            txt.write(text)

def scrape(pdffile,dirs):
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
        subprocess.run(['mv',txtfile,dirs['scraped']])
    else:
        subprocess.run(['cp',pdffile,dirs['noscrape']])
        subprocess.run(['rm',txtfile])

def get_pdfs(target):
    gl = glob.glob(target + '/*.pdf')
    print(gl)
    return gl

def init_argparser():
    parser = argparse.ArgumentParser(description="Scrapes scrapable pdfs and OCRs those that are not, separating the two.")
    parser.add_argument('target')
    parser.add_argument('-o','--output')
    parser.add_argument('-b','--batch',action='store_true')
    return parser

def init_dirs(output_dir):
    output_dir = output_dir.strip()
    # print(f'|{output_dir}|')
    dirs = {}
    dirs['scraped'] = output_dir + '/scraped'
    dirs['noscrape'] = output_dir + '/noscrape'
    dirs['ocr_dir'] = output_dir + '/ocr'
    dirs['img_dir'] = output_dir + '/img'
    dirs['forms'] = output_dir + '/forms'

    subprocess.run(['mkdir',output_dir])
    for dir in dirs.values():
        subprocess.run(['mkdir',dir])
    return dirs

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

def run(target,batch=False,output=OUTPUT_FOLDER_DEFAULT):
    parser = init_argparser()
    if batch: 
        args = parser.parse_args([target,'-b',f'-o {output}'])
    else:
        args = parser.parse_args([target,f'-o {output}'])
    
    start(args)

if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    # print(args)
    start(args)
    