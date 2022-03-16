
from datetime import datetime
from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from custom_logger import CustomLogger
from userRouter import User


def authenticate_token(token):
    print(token)
    print(User.user_tokens)
    if token not in User.user_tokens:
        return (False, "", "")
    
    return (True, token, User.user_tokens[token])

generator_args_parser = reqparse.RequestParser()
generator_args_parser.add_argument("time", type=str)
#Funkcije koje zeljko treab da napravi pocinju slovom Z

class Generator(Resource):

    logger = CustomLogger()

    def get(self, genNum, token):
        if not authenticate_token(token)[0]:
            return Response(None, 405)
        #Ovde se pribavljaju infomracije o generatoru (stanje senzora1 i senzora2 i da li se generator puni ili prazni)
        #state je promenjiva koja cuva stanja, ovo treba da vrati Zeljkova funkcija koja cita stanja generatora
        state = {
            "senzor1": False,
            "senzor2": True,
            "stanje": "neutralno"
        }

        #state = ZgetSenzorData(genNum)
        return make_response(jsonify(state), 200)
        
    def post(self, genNum, token):
        if not authenticate_token(token)[0] or authenticate_token(token)[2][0]!="upravljac":
            return Response(None, 405)

        time = generator_args_parser.parse_args()['time']
        name = authenticate_token(token)[2][1]
        #post metoda koja scheduluje pravnjenje za navedeni generator
        #Ovde se poziva Zeljkov kod koji scheduluje da se izvrsi punujenje i praznjenje
        if not time:
            return Response(None, 403)
        if not Generator.logger.check_availability(time):
            return Response(None, 403)

        print(time)
        isSuccsessful = True
        #Zeljko, ova funkcija treab da vraca True ako je uspesno zakazano praznjenje i punjenje
        #isSuccsessful = ZzakaziOperaciju(genNum, time)
        if isSuccsessful:
            Generator.logger.enter_log(time, name)
            return Response(None, 200)
        else:
            return Response(None, 500)
    