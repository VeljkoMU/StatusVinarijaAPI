
from datetime import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

generator_args_parser = reqparse.RequestParser()
generator_args_parser.add_argument("time", type=int)


class Generator(Resource):
    def get(self, genNum):
        #Ovde se pribavljaju infomracije o generatoru (stanje senzora1 i senzora2 i da li se generator puni ili prazni)
        #state je promenjiva koja cuva stanja, ovo treba da vrati Zeljkova funkcija koja cita stanja generatora
        state = {
            "senzor1": 0,
            "senzor2": 0,
            "stanje": "neutralno"
        }
        return make_response(jsonify(state), 200)
    def post(self, genNum):
        time = generator_args_parser.parse_args()['time']
        #post metoda koja scheduluje pravnjenje za navedeni generator
        #Ovde se poziva Zeljkov kod koji scheduluje da se izvrsi punujenje i praznjenje
        print(time)
        return 200
    