import jwtutils
import arguments
import pdf2png
import qrcodereader

def main():
    # retrieving command line arguments
    args = arguments.getArguments()

    # call the appropriate function depending on the command line argument passed
    if args.pdf:
        # converting the government-issued PDF to a PNG
        img = pdf2png.convertPDF(args)

        # read the QR code and extract the SHC string from it
        data = qrcodereader.readQRCodeFromImg(img)

    elif args.img:
        # read the QR code and extract the SHC string from it
        data = qrcodereader.readQRCodeFromImg(args.img)

    else:
        # validate the SHC provided in the command line arguments
        if jwtutils.validateSHC(args.shc):
            data = args.shc


    # convert the SHC representation of the JWT to the actual JWT
    encodedJWT = jwtutils.shcToJWT(data)

    # decoding the JWT header
    jwtutils.decodeAndPrintHeader(encodedJWT)

    # decoding the JWT body
    jwtutils.decodeAndPrintBody(encodedJWT)

if __name__ == "__main__":
    main()