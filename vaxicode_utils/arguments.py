import sys
import argparse

def get_arguments():
    '''utility method that sets the command line arguments and returns the parser result'''

    parser = argparse.ArgumentParser(usage="Vaxicode Parser aims at taking the Québec-issued PDF of your vaccination QR code and extracting the information that is contained in it.")
    parser.add_argument("-p", "--pdf", help="processes the government-issued PDF to convert it into a PNG to detect the QR code and then parse it (slowest)")
    parser.add_argument("-i", "--img", help="processes a PNG image of the QR code and then parse it (slow)")
    parser.add_argument("-s", "--shc", help="processes the SHC string contained in the QR code and then parse it (fastest)")
    validate_arguments(parser)
    return parser.parse_args()

def validate_arguments(parser:argparse.ArgumentParser):
    '''utility method that ensures the help message is displayed if the script is called with no arguments'''

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)