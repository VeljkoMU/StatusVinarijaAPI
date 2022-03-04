from hashlib import md5
from importlib.resources import Resource
from flask_restful import reqparse, Resource

user_data_args_parser = reqparse.RequestParser()
user_data_args_parser.add_argument("username", type=str)
user_data_args_parser.add_argument("password", type=str)

class User(Resource):
    def post(self):
        username = user_data_args_parser.parse_args()["username"]
        password = str(md5(user_data_args_parser.parse_args()["password"].encode("utf-8")).digest())

        print(username + " " + password)

        #Pribavljamo password i username iz baze i vrsimo autorizaciju
        passStored = "testpass"
        if password==passStored:
            #DOzvoljavamo pristup applikaciji
            return 200
        else:
            return 405
