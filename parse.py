from pdf2image import convert_from_path
from pathlib import Path
import cv2
import sys
import jwt
import zlib
import json
import jwtutils

# retrieve the pdf path from the command line arguments
pdfpath = str(sys.argv[1])

# convert government-issued pdf to png for cv2 to detect the qrcode
pages = convert_from_path(pdfpath, 500)
pages[0].save(str(Path("output-files/pngqrcode.png")), "PNG")

# read QRCODE from the converted pdf
img = cv2.imread(str(Path("output-files/pngqrcode.png")))

# initialize the cv2 QRCODE detector
detector = cv2.QRCodeDetector()

# detect and decode QRCODE
data, bbox, straight_qrcode = detector.detectAndDecode(img)

# convert the SHC representation of the JWT to the actual JWT
encoded_jwt = jwtutils.shc_to_jwt(data)

# decoding the JWT header
decoded_header = str(jwt.get_unverified_header(encoded_jwt))

# sanitizing the JSON data to pretty print it
decoded_header = decoded_header.replace("\'", "\"")
decoded_header_formatted = json.dumps(json.loads(decoded_header), indent=4)
print("Header:\n" + decoded_header_formatted)

# decoding the JWT body
decompressed_body = jwtutils.base64_decode(encoded_jwt.split(".")[1])
decoded_body = str(zlib.decompress(decompressed_body, wbits=-15))[2:-1]

# sanitizing the JSON data to pretty print it
decoded_body = decoded_body.replace("\'", "\"").encode('utf-8').decode('unicode_escape').encode('latin-1')
decoded_body_formatted = json.dumps(json.loads(decoded_body), ensure_ascii=False, indent=4)
print("Body:\n" + str(decoded_body_formatted))