from flask import (
    Blueprint, 
    request
)
import json
from api.security.guards import authorization_guard, get_bearer_token_from_request
from api.connection import db
from api.utils import mongo_formatter, json_abort
# https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html
from bson.objectid import ObjectId
from http import HTTPStatus
# https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
# https://stackoverflow.com/questions/38967706/pymongo-global-name-returndocument-is-not-defined
from pymongo import ReturnDocument
from api.security.user import user_from_token
# https://auth0.com/docs/quickstart/spa/react/01-login#install-the-auth0-react-sdk
bp_name = 'api-cart'
bp_url_prefix = '/api/cart'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)
# https://py.processing.org/reference/indexbrackets.html#:~:text=Index%20brackets%20(%5B%5D)%20have%20many,single%20character%20in%20a%20string.

# @bp.route("/")
# @authorization_guard
# def cart():
#     return {}
# https://docs.python.org/3/library/json.html
# displaying the whole cart
@bp.route("/", methods=["GET"])
@authorization_guard
def cart_get():
    # myuser is a dictionary
    #json.dumps converts objects into json string
    results = db.carts.find({"user": get_email()})
    return json.dumps(merge_cart_with_product_data(results))
    # return str(list(db.carts.find({"user": userid})))
    # return  list(db.carts.find({"user": userid}))
# we dont need the userid because the userid is the accesstoken from auth0


# # current response
# [
#     {
#         "_id" : ObjectId("63817d8ff78998a339659553"),
#         "user" : "danielyaghoobian@gmail.com",
#         "product_id" : ObjectId("637bffec0fd0cbc39d762fd0"),
#         "quantity" : 1
#     }
# ]
#rubber duck method alternative - speak to audience
# # what we want
# [
#     {
#         "_id" : ObjectId("637bffec0fd0cbc39d762fd0"),
#         "name" : "Ring Camera",
#         "image" : "https://m.media-amazon.com/images/I/41Hc4IGGzdL._SX425_.jpg"
#         "quantity": 1
#     }
# ]

def merge_cart_with_product_data(data):
    results = []

    # product_ids will be a list of product_ids in the cart
    product_ids = []

    # quantity_map will be a map of product_id to quantity in cart
    quantity_map = {}

    # quantity_map = {"637bffec0fd0cbc39d762fd0": 1}
    # loop through current docs and populate product_ids and quantity_map
    for doc in data:
        product_ids.append(doc["product_id"])
    # had to add str to make the object id into a string to get the key
        quantity_map[str(doc["product_id"])] = doc["quantity"]

    # query that will query the products collection for a list of products
    product_query = {
        "_id" : { "$in": product_ids}
    }

    # query database
    products = db.products.find(product_query)
    # print(quantity_map)
    # loop through documents adding a key called quantity to the results
    for doc in products:
        filtered_doc = mongo_formatter(doc)
        # print('doc',doc)
        # get returns the value
        filtered_doc["quantity"] = quantity_map.get(doc["_id"])
        results.append(filtered_doc)
    return results




def get_email():
    token = get_bearer_token_from_request()
    myuser = user_from_token(token)
    return myuser["email"]

# Get product
@bp.route("/product/<productid>", methods=["GET"])
@authorization_guard
def product_get(productid):
    results = db.carts.find_one({"user": get_email(), "product_id": ObjectId(productid)})
    return json.dumps(mongo_formatter(results))

# Delete product 
@bp.route("/product/<productid>", methods=["DELETE"])
@authorization_guard
def product_delete(productid):
    results = db.carts.find_one_and_delete({"user": get_email(), "product_id": ObjectId(productid)})
    return json.dumps(mongo_formatter(results))

# post product
# https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask'
@bp.route("/product/<productid>", methods=["POST"])
@authorization_guard
def product_insert(productid):
    content = request.get_json()
    quantity = content.get('quantity')
    if not quantity:
        invalid_request_error = {
            "error": "invalid_request",
            "error_description": "need quantity passed",
            "message": "Requires quantity"
        }
#json abort from auth0 docs
        json_abort(HTTPStatus.BAD_REQUEST, invalid_request_error)


    # print(content)
    # else:
    #     if quantity > 0:
    #         invalid_request_error = {
    #             "error": "invalid_request",
    #             "error_description": "need quantity passed",
    #             "message": "Requires quantity"
    #         }
    #         json_abort(HTTPStatus.BAD_REQUEST, invalid_request_error)

    document = {
        "user": get_email(),
        "product_id": ObjectId(productid),
        "quantity": quantity
    }
    db.carts.insert_one(document)
    return json.dumps(mongo_formatter(document))
#update quantity
@bp.route("/product/<productid>", methods=["PATCH"])
@authorization_guard
def product_update(productid):
    content = request.get_json()
    quantity = content.get('quantity')
    if not quantity:
        invalid_request_error = {
            "error": "invalid_request",
            "error_description": "need quantity passed",
            "message": "Requires quantity"
        }
        json_abort(HTTPStatus.BAD_REQUEST, invalid_request_error)
    
    document = {
        "user": get_email(),
        "product_id": ObjectId(productid),
    }

    found_document = db.carts.find_one(document)
    # https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
    if not found_document:
        not_found_error = {
            "error": "not_found",
            "error_description": "no document found, can't update quantity",
            "message": "no matching document"
        }
        json_abort(HTTPStatus.NOT_FOUND, not_found_error)
    # https://www.geeksforgeeks.org/python-mongodb-find_one_and_update-query/
    new_document = db.carts.find_one_and_update({
        '_id': found_document['_id']
    }, { "$set": { 'quantity': quantity } }, return_document = ReturnDocument.AFTER)
    return json.dumps(mongo_formatter(new_document))