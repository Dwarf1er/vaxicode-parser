import cv2
import argparse
import numpy
import re
import base64
import zlib
import json
import os
from pdf2image import convert_from_path
from typing import List

parser = argparse.ArgumentParser(
    description=("Decode Smart Health Card information from QR codes "
                 "in PDFs, images or SHC strings.")
)
parser.add_argument("--pdf", help="Path to the PDF file")
parser.add_argument("--image", help="Path to the image file")
parser.add_argument("--shc", help="SHC string")


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    return parser.parse_args()


def pdf_to_image(pdf_path: str) -> numpy.ndarray:
    """
    Convert the first page of a PDF to a numpy array image.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        numpy.ndarray: Numpy array representing the image.
    """
    pages = convert_from_path(pdf_path, 500)
    return numpy.array(pages[0])


def read_qr_code(image_data: numpy.ndarray) -> str:
    """
    Read the QR code from an image and decode it.

    Args:
        image_data (numpy.ndarray): Numpy array representing the image.

    Returns:
        str: Decoded information from the QR code.
    """
    image: numpy.ndarray = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    detect: cv2.QRCodeDetector = cv2.QRCodeDetector()
    value, _, _ = detect.detectAndDecode(image)
    return value


def read_qr_code_from_file(image_path: str) -> str:
    """
    Read the QR code from an image file and decode it.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Decoded information from the QR code.
    """
    image: numpy.ndarray = cv2.imread(image_path)
    detect: cv2.QRCodeDetector = cv2.QRCodeDetector()
    value, _, _ = detect.detectAndDecode(image)
    return value


def shc_to_jwt(shc_string: str) -> str:
    """
    Convert a Smart Health Card (SHC) string to a JSON Web Token (JWT).

    Args:
        shc_string (str): SHC string containing encoded health information.

    Returns:
        str: JWT string containing decoded health information.
    """
    integer_pairs: List[str] = [
        (shc_string[i:i+2]) for i in range(5, len(shc_string), 2)]
    base10_pairs: List[int] = [int(i, base=10) for i in integer_pairs]
    ascii_values_offset: List[str] = [chr(i + 45) for i in base10_pairs]
    jwt: str = ""
    for i in ascii_values_offset:
        jwt += i
    jwt = re.sub("/[^0-9]/", "", jwt)
    return jwt


def decode_jwt(jwt: str) -> None:
    """
    Decode a JSON Web Token (JWT) and print the decoded header and payload.

    Args:
        jwt (str): JWT string containing encoded health information.

    Returns:
        None: This function does not return any value.
    """
    header, payload, _ = jwt.split(".")

    decoded_header = base64.urlsafe_b64decode(header + "==").decode("utf-8")

    payload_bytes = payload.encode("utf-8")
    missing_padding = len(payload_bytes) % 4
    if missing_padding:
        payload_bytes += b"=" * (4 - missing_padding)

    decoded_payload = zlib.decompress(
        base64.urlsafe_b64decode(payload_bytes),
        wbits=-15
    ).decode("utf-8")

    decoded_header = json.loads(decoded_header)
    decoded_payload = json.loads(decoded_payload)

    print(json.dumps(decoded_header, indent=4))
    print(json.dumps(decoded_payload, indent=4))


def main() -> None:
    """
    Main function to parse command line arguments and decode SHC information.
    """
    args = parse_args()

    if args.pdf:
        pdf_path = os.path.abspath(args.pdf)
        print(f"Processing PDF: {pdf_path}")
        image_data: numpy.ndarray = pdf_to_image(pdf_path)
        shc: str = read_qr_code(cv2.imencode(".jpg", image_data)[1])
    elif args.image:
        image_path = os.path.abspath(args.image)
        print(f"Processing image: {image_path}")
        shc: str = read_qr_code_from_file(image_path)
    elif args.shc:
        print("Processing SHC string")
        shc: str = args.shc
    else:
        parser.print_help()
        return

    jwt: str = shc_to_jwt(shc)
    decode_jwt(jwt)


if __name__ == "__main__":
    main()
