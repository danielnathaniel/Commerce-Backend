from auth0.v3.authentication import Users

from flask import (
    Blueprint
)

from api.security.guards import authorization_guard, get_bearer_token_from_request
from common.utils import safe_get_env_var

auth0_domain = safe_get_env_var("AUTH0_DOMAIN")
# domain = 'dev-i7xqutftfyxkoc86.us.auth0.com'
bp_name = 'api-profile'
bp_url_prefix = '/api/profile'
bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix)


@bp.route("/")
@authorization_guard
def profile():
    token = get_bearer_token_from_request()
    # print(token)
    users = Users(auth0_domain)
    myuser = users.userinfo(token) 
    # print(myuser)

    # print('profile route working')
    return myuser

