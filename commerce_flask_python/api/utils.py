from flask import jsonify, abort
import bson

def json_abort(status_code, data=None):
    response = jsonify(data)
    response.status_code = status_code
    abort(response)

def mongo_formatter(data):
    if isinstance(data, dict):
        return format_dict(data)
    
    results = []
    for x in data:
        # for key, value in x.items():
        #     if bson.ObjectId.is_valid(value):
        #         x[key] = str(value)
        new_dict = format_dict(x)
        results.append(new_dict)
    return results
    

def format_dict(data):
    for key, value in data.items():
        if bson.ObjectId.is_valid(value):
            data[key] = str(value)
    return data