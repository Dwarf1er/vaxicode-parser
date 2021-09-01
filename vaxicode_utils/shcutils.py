import re

def validate_SHC_format(shc:str) -> bool:
    '''utility method to validate the format of SHCs passed as command line argument'''

    if not shc.startswith("shc:/"):
        print("ERROR: SHCs are expected to start with the prefix 'shc:/[...]'")
        return False
    if len(shc[5:]) % 2 != 0:
        print("ERROR: SHCs are expected to have an even length")
        return False
    if not shc[5:].isnumeric():
        print("ERROR: SHCs are expected to contain only integers")
        return False
    return True

def SHC_to_JWT(shc:str)-> str:
    '''utility method to convert the SHC representation of the JWT to the actual JWT'''

    # split the shc in pairs of 2 integers
    split2 = [(shc[i:i+2]) for i in range(5, len(shc), 2)]

    # convert the pairs of integers to base10 ASCII values
    base10 = [int(i, base=10) for i in split2]

    # convert the base10 ASCII values to their characters with an offset of 45
    # the offset of 45 is part of the SHC standard implementation
    ascii_values = [chr(i + 45) for i in base10]

    encoded_JWT = ""
    for i in ascii_values:
        encoded_JWT += i
    encoded_JWT = re.sub("/[^0-9]/", "", encoded_JWT)
    return encoded_JWT