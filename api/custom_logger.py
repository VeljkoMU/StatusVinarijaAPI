
from flask import jsonify
from db import get_db


class CustomLogger:
    def __init__(self):
        self.db= get_db()
        self.collection_log = self.db["op-log"]
    
    def enter_log(self, time, name):
        self.collection_log.insert_one({
            "time": time,
            "user": name,
            "date": time[0:10],
            "hours": int(time[11:13])
        })
    
    def check_availability(self, time):
        log = self.collection_log.find_one({"time": time})

        if log:
            return False
        else:
            date = time[0:10]
            hours = int(time[11:13])
            s1 = self.collection_log.find({"date": date})
            if not s1:
                return True
            for i in s1:
                if i["hours"]==hours or i["hours"]-1 == hours:
                    return False
            return True
