from vaxicode_utils import arguments, pdf2png, qrcodereader, shcutils, jwtutils

def main():
    # retrieving command line arguments
    args = arguments.get_arguments()

    # call the appropriate function depending on the command line argument passed
    if args.pdf:
        # converting the government-issued PDF to a PNG
        img = pdf2png.convert_PDF(args)

        # read the QR code and extract the SHC string from it
        data = qrcodereader.read_QR_code_from_img(img)

    elif args.img:
        # read the QR code and extract the SHC string from it
        data = qrcodereader.read_QR_code_from_img(args.img)

    else:
        # validate the SHC provided in the command line arguments
        if shcutils.validate_SHC_format(args.shc):
            data = args.shc
        else:
            return


    # convert the SHC representation of the JWT to the actual JWT
    encoded_JWT = shcutils.SHC_to_JWT(data)

    # decoding the JWT header
    jwtutils.decode_and_print_header(encoded_JWT)

    # decoding the JWT body
    jwtutils.decode_and_print_body(encoded_JWT)

if __name__ == "__main__":
    main()