from pathlib import Path
import cv2

def readQRCodeFromImg(img):
    # read QRCODE from the converted pdf
    img = cv2.imread(str(Path(img)))

    # initialize the cv2 QRCODE detector
    detector = cv2.QRCodeDetector()

    # detect and decode QRCODE
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    return data