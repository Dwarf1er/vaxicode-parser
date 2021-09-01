from pathlib import Path
import cv2

def read_QR_code_from_img(img:str):
    '''utility method to read the QR code contained in a PNG image'''

    # read QRCODE from the converted pdf
    img = cv2.imread(str(Path(img)))

    # initialize the cv2 QRCODE detector
    detector = cv2.QRCodeDetector()

    # detect and decode QRCODE
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    return data