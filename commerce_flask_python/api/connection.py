from pymongo import MongoClient    
from common.utils import safe_get_env_var

mongouri = safe_get_env_var("MONGOURI")
mongodb = safe_get_env_var("DATABASENAME")
db = MongoClient(mongouri)[mongodb]
# print("db write", db.write_concern)