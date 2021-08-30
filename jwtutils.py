from typing import Union
import base64
import re

# utility method to decompress raw DEFLATE compressed strings
def base64_decode(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str): data = data.encode('utf8')

    missing_padding = len(data) % 4

    if missing_padding:
        data += b"=" * (4 - missing_padding)

    return base64.urlsafe_b64decode(data)

# utility method to convert the SHC representation of the JWT to the actual JWT
def shc_to_jwt(shc):

    # split the shc in pairs of 2 integers
    split2 = [(shc[i:i+2]) for i in range(5, len(shc), 2)]

    # convert the pairs of integers to base10 ASCII values
    base10 = [int(i, base=10) for i in split2]

    # convert the base10 ASCII values to their characters with an offset of 45
    # the offset of 45 is part of the SHC standard implementation
    ascii_values = [chr(i + 45) for i in base10]

    encoded_jwt = ""
    for i in ascii_values:
        encoded_jwt += i
    encoded_jwt = re.sub("/[^0-9]/", "", encoded_jwt)
    return encoded_jwt