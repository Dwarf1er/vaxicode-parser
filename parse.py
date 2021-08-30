from pdf2image import convert_from_path
import cv2
import sys
import jwt
import zlib
import json
import jwtutils

# retrieve the pdf path from the command line arguments
pdfpath = str(sys.argv[1])

# convert government-issued pdf to png for cv2 to detect the qrcode
pages = convert_from_path(pdfpath, 500, poppler_path=r".\poppler-21.08.0\Library\bin")
pages[0].save("output-files\pngqrcode.png", "PNG")

# read QRCODE from the converted pdf
img = cv2.imread("output-files\pngqrcode.png")

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
test = json.loads(decoded_header)
test2 = json.dumps(test, indent=4)
print("Header:\n" + test2)

# decoding the JWT body
decompressed_body = jwtutils.base64_decode(encoded_jwt.split(".")[1])
decoded_body = str(zlib.decompress(decompressed_body, wbits=-15))[2:-1]

# sanitizing the JSON data to pretty print it
decoded_body = decoded_body.replace("\'", "\"").replace("\\xc3\\x89", "E")
decoded_body_formatted = json.dumps(json.loads(decoded_body), indent=4)
print("Body:\n" + decoded_body_formatted)