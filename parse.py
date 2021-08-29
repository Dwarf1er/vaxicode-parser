from pdf2image import convert_from_path
import cv2
import sys
import re
import jwt
import zlib
import base64

# retrieve the pdf path from the command line arguments
pdfpath = str(sys.argv[1])

# convert government-issued pdf to png for cv2 to detect the qrcode
pages = convert_from_path(pdfpath, 500, poppler_path=r".\poppler-21.08.0\Library\bin")
pages[0].save("pngqrcode.png", "PNG")

# read QRCODE from the converted pdf
img = cv2.imread("pngqrcode.png")

# initialize the cv2 QRCODE detector
detector = cv2.QRCodeDetector()

# detect and decode QRCODE
data, bbox, straight_qrcode = detector.detectAndDecode(img)

# convert the SHC representation of the JTW to the actual JWT
split2 = [(data[i:i+2]) for i in range(5, len(data), 2)]
split2 = [int(i, base=10) for i in split2]
split2 = [chr(i + 45) for i in split2]
encoded_jwt = ""
for i in split2:
    encoded_jwt += i
encoded_jwt = re.sub("/[^0-9]/", "", encoded_jwt)

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

# decoding the JWT headers
decoded_header = jwt.get_unverified_header(encoded_jwt)
print("Header:\n" + str(decoded_header))

# decoding the JTW body
# decoded_body = jwt.decode(encoded_jwt, options={"verify_signature": False}, algorithms=["ES256"])
body = b""
decoded_body = decode_base64_and_inflate(body)
print("Body:\n" + decoded_body)