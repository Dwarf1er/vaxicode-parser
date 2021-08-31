import sys
import argparse

# utility method that sets the command line arguments and returns the parser result
def getArguments():
    # defining command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pdf", help="processes the government-issued PDF to convert it into a PNG to detect the QR code and then parse it (slowest)")
    parser.add_argument("-i", "--img", help="processes a PNG image of the QR code and then parse it (slow)")
    parser.add_argument("-s", "--shc", help="processes the SHC string contained in the QR code and then parse it (fastest)")
    validateArguments(parser)
    return parser.parse_args()

# utility method that ensures the help message is displayed if the script is called with no arguments
def validateArguments(parser):
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)