

from flask import make_response
from flask_restful import Resource


class Preditions(Resource):
    def calcPred(self):
        #Ovde ce biti implementirano izracunavanje dobitna 
        return 1
    
    def get(self):
        return make_response(self.calcPred(), 200)
    
    