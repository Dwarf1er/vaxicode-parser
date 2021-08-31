from pdf2image import convert_from_path
from pathlib import Path

# utility method to retrieve the pdf path from the command line arguments
def getPDFPath(args):
    pdfPath = args.pdf
    return pdfPath

# utility method to convert the government-issued PDF to PNG for cv2 to detect the qrcode
def convertPDF(args):
    pages = convert_from_path(getPDFPath(args), 500)
    pages[0].save(str(Path("output-files/pngqrcode.png")), "PNG")
    return str(Path("output-files/pngqrcode.png"))