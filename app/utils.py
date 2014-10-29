from flask import jsonify

def enum(**enums):
    return type('Enum', (), enums)

def make_json_resp(code, **kwargs):
    resp = jsonify(**kwargs)
    resp.status_code = code
    return resp