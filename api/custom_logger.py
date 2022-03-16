
from flask import jsonify
from db import get_db


class CustomLogger:
    def __init__(self):
        self.db= get_db()
        self.collection_log = self.db["op-log"]
    
    def enter_log(self, time, name):
        self.collection_log.insert_one({
            "time": time,
            "user": name
        })
    
    def check_availability(self, time):
        log = self.collection_log.find_one({"time": time})

        if log:
            return False
        else:
            t = log["time"]
            print(t)
            return True
