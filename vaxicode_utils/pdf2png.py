from pdf2image import convert_from_path
from pathlib import Path
import os

def get_PDF_path(args:str):
    '''utility method to retrieve the pdf path from the command line arguments'''

    pdfPath = args.pdf
    return pdfPath

def convert_PDF(args:str):
    '''utility method to convert the government-issued PDF to PNG for cv2 to detect the qrcode'''
    
    if not os.path.exists(Path("output_files")):
        os.mkdir(Path("output_files"))
    
    pages = convert_from_path(get_PDF_path(args), 500)
    pages[0].save(str(Path("output_files/pngqrcode.png")), "PNG")
    return str(Path("output_files/pngqrcode.png"))