import cv2
import argparse
import numpy
import re
import base64
import zlib
import json
from pdf2image import convert_from_path

parser = argparse.ArgumentParser(
    description="Process PDFs, images, or SHC strings."
)
parser.add_argument("--pdf", help="Path to the PDF file")
parser.add_argument("--image", help="Path to the image file")
parser.add_argument("--shc", help="SHC string")


def parse_args():
    return parser.parse_args()


def pdf_to_image(pdf_path):
    pages = convert_from_path(pdf_path, 500)
    image_data = numpy.array(pages[0])
    return image_data


def read_qr_code(image_data):
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    return value


def read_qr_code_from_file(image_path):
    img = cv2.imread(image_path)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    return value


def shc_to_jwt(shc_string):
    integer_pairs = [(shc_string[i:i+2]) for i in range(5, len(shc_string), 2)]
    base10_pairs = [int(i, base=10) for i in integer_pairs]
    ascii_values_offset = [chr(i + 45) for i in base10_pairs]
    jwt = ""
    for i in ascii_values_offset:
        jwt += i
    jwt = re.sub("/[^0-9]/", "", jwt)
    return jwt


def decode_jwt(jwt):
    header, payload, _ = jwt.split(".")

    decoded_header = base64.urlsafe_b64decode(header + "==").decode("utf-8")

    payload = payload.encode("utf-8")
    missing_padding = len(payload) % 4
    if missing_padding:
        payload += b"=" * (4 - missing_padding)

    decoded_payload = zlib.decompress(
        base64.urlsafe_b64decode(payload),
        wbits=-15
    ).decode("utf-8")

    decoded_header = json.loads(decoded_header)
    decoded_payload = json.loads(decoded_payload)

    print(json.dumps(decoded_header, indent=4))
    print(json.dumps(decoded_payload, indent=4))


def main():
    args = parse_args()

    if args.pdf:
        print(f"Processing PDF: {args.pdf}")
        image_data = pdf_to_image(args.pdf)
        shc = read_qr_code(cv2.imencode(".jpg", image_data)[1])
    elif args.image:
        print(f"Processing image: {args.image}")
        shc = read_qr_code_from_file(args.image)
    elif args.shc:
        print(f"Processing SHC string: {args.shc}")
        shc = args.shc
    else:
        parser.print_help()

    jwt = shc_to_jwt(shc)
    decode_jwt(jwt)


if __name__ == "__main__":
    main()
