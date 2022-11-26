from pymongo import MongoClient    

mongouri = 'mongodb+srv://danielyaghoobian:PghRPWK8ob2qqTz8@cluster0.ms8sspi.mongodb.net'

db = MongoClient(mongouri)["commerce"]