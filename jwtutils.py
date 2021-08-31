from typing import Union
import base64
import re
import sys
import zlib
import jwt
import jsonutils

# utility method to decode raw DEFLATE compressed strings
def base64_decode(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str): data = data.encode('utf8')

    missing_padding = len(data) % 4

    if missing_padding:
        data += b"=" * (4 - missing_padding)

    return base64.urlsafe_b64decode(data)

# utility method to convert the SHC representation of the JWT to the actual JWT
def shcToJWT(shc):

    # split the shc in pairs of 2 integers
    split2 = [(shc[i:i+2]) for i in range(5, len(shc), 2)]

    # convert the pairs of integers to base10 ASCII values
    base10 = [int(i, base=10) for i in split2]

    # convert the base10 ASCII values to their characters with an offset of 45
    # the offset of 45 is part of the SHC standard implementation
    asciiValues = [chr(i + 45) for i in base10]

    encodedJWT = ""
    for i in asciiValues:
        encodedJWT += i
    encodedJWT = re.sub("/[^0-9]/", "", encodedJWT)
    return encodedJWT

# utility method to validate SHCs
def validateSHC(shc):
    if shc.startswith("shc:/"):
        return True
    else:
        print("The SHC provided in the command line arguments is not a valid SHC, it should start with 'shc:/[...]'\nExiting... Please try again")
        sys.exit(1)

# utility method to decode and print the header of the JWT
def decodeAndPrintHeader(encodedJWT):
    # decoding the JWT header
    decodedHeader = str(jwt.get_unverified_header(encodedJWT))

    # sanitizing the JSON data to pretty print it
    decodedHeader = jsonutils.sanitizeJSON(decodedHeader)
    decodedHeaderFormatted = jsonutils.formatJSON(decodedHeader)
    print("Header:\n" + decodedHeaderFormatted)

# utility method to decode and print the body of the JWT
def decodeAndPrintBody(encodedJWT):
    # decoding the JWT header
    decodedBody = str(zlib.decompress(base64_decode(encodedJWT.split(".")[1]), wbits=-15))[2:-1]

    # sanitizing the JSON data to pretty print it
    decodedBody = jsonutils.sanitizeJSON(decodedBody)
    decodedBodyFormatted = jsonutils.formatJSON(decodedBody)
    print("Body:\n" + decodedBodyFormatted)