from flask import jsonify

def enum(**enums):
    return type('Enum', (), enums)

def make_json_resp(code=None, **kwargs):
    resp = jsonify(**kwargs)
    if code is not None:
        resp.status_code = code
    return resp

class DuplicateSuggestionError(Exception):
    pass
