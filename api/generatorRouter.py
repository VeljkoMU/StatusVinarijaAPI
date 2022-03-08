
from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

generator_args_parser = reqparse.RequestParser()
generator_args_parser.add_argument("time", type=int)
#Funkcije koje zeljko treab da napravi pocinju slovom Z

class Generator(Resource):
    def get(self, genNum):
        #Ovde se pribavljaju infomracije o generatoru (stanje senzora1 i senzora2 i da li se generator puni ili prazni)
        #state je promenjiva koja cuva stanja, ovo treba da vrati Zeljkova funkcija koja cita stanja generatora
        state = {
            "senzor1": 0,
            "senzor2": 0,
            "stanje": "neutralno"
        }

        state = ZgetSenzorData(genNum)
        return make_response(jsonify(state), 200)
        
    def post(self, genNum):
        time = generator_args_parser.parse_args()['time']
        #post metoda koja scheduluje pravnjenje za navedeni generator
        #Ovde se poziva Zeljkov kod koji scheduluje da se izvrsi punujenje i praznjenje
        if not time:
            return 403
        print(time)
        #Zeljko, ova funkcija treab da vraca True ako je uspesno zakazano praznjenje i punjenje
        isSuccsessful = ZzakaziOperaciju(genNum, time)
        if isSuccsessful:
            return 200
        else:
            return 500
    