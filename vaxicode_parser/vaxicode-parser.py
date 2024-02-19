import cv2
import argparse
import numpy
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
    # pages[0].save(".\\image.png", "PNG")
    image_data = numpy.array(pages[0])
    return image_data


def read_qr_code(image_data):
    # img = cv2.imread(image_path)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    return value


def main():
    args = parse_args()

    if args.pdf:
        print(f"Processing PDF: {args.pdf}")
        image_data = pdf_to_image(args.pdf)
        qr_data = read_qr_code(cv2.imencode(".jpg", image_data)[1])
        print(qr_data)
    elif args.image:
        print(f"Processing image: {args.image}")
        # Add image processing logic here
    elif args.shc:
        print(f"Processing SHC string: {args.shc}")
        # Add SHC string processing logic here
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
