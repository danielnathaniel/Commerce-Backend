from api.connection import db
from api.utils import mongo_formatter
import json
from bson.objectid import ObjectId
from flask import (
    Blueprint
)
# use app.run! ! https://stackoverflow.com/questions/73183394/view-function-did-not-return-a-valid-response-the-return-type-must-be-a-string
bp_name = 'api-products'
bp_url_prefix = '/api/products'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route("", methods=["GET"])
def products():
    results = db.products.find()
    return json.dumps(mongo_formatter(results))
    # leaving find blank returns everything from the collections
    # find returns an iterator causing problems - list puts it into an array 


@bp.route("/<productid>", methods=["GET"])
def singleproduct(productid):
    results = db.products.find_one({
        "_id": ObjectId(productid),
    })
    return json.dumps(mongo_formatter(results))
