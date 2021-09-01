import json

def sanitize_JSON(data:str) -> str:
    '''utility method to sanitize the JWT contents before printing to JSON format'''

    return data.replace("\'", "\"")

def format_JSON(data:str) -> str:
    '''utility method to print the JWT contents to JSON format'''

    return json.dumps(json.loads(data), ensure_ascii=False, indent=4)