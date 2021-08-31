import json

def sanitizeJSON(data):
    return data.replace("\'", "\"").encode('utf-8').decode('unicode_escape').encode('latin-1')

def formatJSON(data):
    return json.dumps(json.loads(data), indent=4)