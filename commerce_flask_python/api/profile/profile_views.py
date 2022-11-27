from auth0.v3.authentication import Users
from api.security.user import user_from_token
from flask import (
    Blueprint
)

from api.security.guards import authorization_guard, get_bearer_token_from_request

# domain = 'dev-i7xqutftfyxkoc86.us.auth0.com'
bp_name = 'api-profile'
bp_url_prefix = '/api/profile'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route("/")
@authorization_guard
def profile():
    # print(token)
    token = get_bearer_token_from_request()
    myuser = user_from_token(token) 
    # print(myuser)

    # print('profile route working')
    return myuser

