from typing import Union
import base64
import zlib
import jwt
from .jsonutils import *

def base64_decode(data: Union[str, bytes]) -> bytes:
    '''utility method to decode raw DEFLATE compressed strings'''

    if isinstance(data, str): data = data.encode('utf8')

    missing_padding = len(data) % 4

    if missing_padding:
        data += b"=" * (4 - missing_padding)

    return base64.urlsafe_b64decode(data)

def decode_and_print_header(encoded_JWT:str):
    '''utility method to decode and print the header of the JWT'''

    # decoding the JWT header
    decoded_header = str(jwt.get_unverified_header(encoded_JWT))

    # sanitizing the JSON data to pretty print it
    decoded_header = sanitize_JSON(decoded_header)
    decoded_header_formatted = format_JSON(decoded_header)
    print("Header:\n" + decoded_header_formatted)

def decode_and_print_body(encoded_JWT:str):
    '''utility method to decode and print the body of the JWT'''
    
    # decoding the JWT header
    decoded_body = str(zlib.decompress(base64_decode(encoded_JWT.split(".")[1]), wbits=-15))[2:-1]

    # sanitizing the JSON data to pretty print it
    decoded_body = sanitize_JSON(decoded_body)
    decoded_body_formatted = format_JSON(decoded_body)
    print("Body:\n" + decoded_body_formatted)