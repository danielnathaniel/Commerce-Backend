from auth0.v3.authentication import Users
from common.utils import safe_get_env_var
auth0_domain = safe_get_env_var("AUTH0_DOMAIN")

TOKEN_CACHE={}
# getting the user to pass around 
def user_from_token(token):
    cached_user = TOKEN_CACHE.get(token)
    if cached_user:
        return cached_user
    users = Users(auth0_domain)
    myuser = users.userinfo(token)
    TOKEN_CACHE[token] = myuser
    return myuser