import pymongo as mongodb
from tinydb import TinyDB, Query


# CONNECTION_STRING = "mongodb://localhost:27017/StatusVinarija"
# mongoClient = mongodb.MongoClient(CONNECTION_STRING)

db_user_data = TinyDB("userdata.json")
db_logs = TinyDB("logs.json")



def get_db_user():
    return db_user_data

def get_db_logs():
    return db_logs