from flask import jsonify, abort
import bson

def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)
# https://stackabuse.com/python-check-if-variable-is-a-dictionary/
def mongo_formatter(data):
    if isinstance(data, dict):
        return format_dict(data)
    
    results = []
    for x in data:
        new_dict = format_dict(x)
        results.append(new_dict)
    return results
    
# https://stackoverflow.com/questions/28774526/how-to-check-that-mongo-objectid-is-valid-in-python
def format_dict(data):
    for key, value in data.items():
        if bson.ObjectId.is_valid(value):
            data[key] = str(value)
    return data