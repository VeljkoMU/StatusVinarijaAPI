from hashlib import md5
from importlib.resources import Resource
from flask import Response, jsonify, make_response
from flask_restful import reqparse, Resource
import random
import string
from db import get_db




user_data_args_parser = reqparse.RequestParser()
user_data_args_parser.add_argument("username", type=str)
user_data_args_parser.add_argument("password", type=str)

class User(Resource):

    user_tokens=dict()

    def post(self):
        print(user_data_args_parser.parse_args()["password"])
        username = user_data_args_parser.parse_args()["username"]
        password = str(md5(user_data_args_parser.parse_args()["password"].encode("utf-8")).hexdigest())

        print(username + " " + password)

        db=get_db()

        collection_user = db["user-data"]
        user_data = collection_user.find_one({"username": username})

        if user_data:
            if user_data["password"] == password:
                return make_response(jsonify({"token": self.token_generator(username)}), 200)
            else:
                return Response(None, 405)
        else:
            return Response(None, 404)


        #Pribavljamo password i username iz baze i vrsimo autorizaciju
        passStored = "testpass"
        if password==passStored:
            #DOzvoljavamo pristup applikaciji
            return 200
        else:
            return 405

    def token_generator(self, username):
        chars = string.ascii_letters + string.octdigits
        token = ""
        token = token.join(random.choice(chars) for i in range (0,13))

        User.user_tokens[token] = username

        print(User.user_tokens)

        return token
