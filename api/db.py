import pymongo as mongodb


CONNECTION_STRING = "mongodb://localhost:27017/StatusVinarija"
mongoClient = mongodb.MongoClient(CONNECTION_STRING)

db = mongoClient["StatusVinarija"]


def get_db():
    return db