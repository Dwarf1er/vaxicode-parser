import json

def sanitize_JSON(data:str) -> str:
    '''utility method to sanitize the JWT contents before printing to JSON format'''

    return data.replace("\'", "\"").encode('utf-8').decode('unicode_escape').encode('latin-1')

def format_JSON(data:str) -> str:
    '''utility method to print the JWT contents to JSON format'''
    
    return json.dumps(json.loads(data), indent=4)