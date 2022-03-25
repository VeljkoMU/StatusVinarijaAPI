
from flask import jsonify
from db import get_db_logs
from tinydb import TinyDB, Query



class CustomLogger:
    def __init__(self):
        self.db= get_db_logs()
    
    def enter_log(self, time, name):
        self.db.insert({
            "time": time,
            "user": name,
            "date": time[0:10],
            "hours": int(time[11:13])
        })
    
    def check_availability(self, time):
        q = Query()
        log = self.db.search(q.time==time)

        if log:
            return False
        else:
            date = time[0:10]
            hours = int(time[11:13])
            s1 = self.db.search(q.date == date)
            if not s1:
                return True
            for i in s1:
                if i["hours"]==hours or i["hours"]-1 == hours:
                    return False
            return True
