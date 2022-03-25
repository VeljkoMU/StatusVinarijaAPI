from hashlib import md5
from importlib.resources import Resource
from flask import Response, jsonify, make_response
from flask_restful import reqparse, Resource
import random
import string
from db import get_db_user
from tinydb import TinyDB, Query




user_data_args_parser = reqparse.RequestParser()
user_data_args_parser.add_argument("username", type=str)
user_data_args_parser.add_argument("password", type=str)
user_data_args_parser.add_argument("name", type=str, required=False)

def authenticate_token(token):
    print(token)
    print(User.user_tokens)
    if token not in User.user_tokens:
        return (False, "", "")
    
    return (True, token, User.user_tokens[token])

class User(Resource):

    user_tokens=dict()

    def post(self, token):
        print(user_data_args_parser.parse_args()["password"])
        username = user_data_args_parser.parse_args()["username"]
        password = str(md5(user_data_args_parser.parse_args()["password"].encode("utf-8")).hexdigest())

        print(username + " " + password)

        if username == "posmatrac":
            return make_response(jsonify({"token": "gggg"}, 200))

        db=get_db_user()

        q = Query()
        user_data = db.search(q.username==username)[0]
        print(user_data)

        if user_data:
                return make_response(jsonify({"token": self.token_generator(username, user_data["name"])}), 200)
        else:
            return Response(None, 404)


    def put(self, token):
        if not authenticate_token(token)[0] or authenticate_token(token)[2][0]!="administrator":
            return Response(None, 405)

        username = user_data_args_parser.parse_args()["username"]
        password = str(md5(user_data_args_parser.parse_args()["password"].encode("utf-8")).hexdigest())
        name = user_data_args_parser.parse_args()["name"]

        db = get_db_user()

        db.insert({
            "username": username,
            "password": password,
            "name": name
        })

    def token_generator(self, username, name):
        chars = string.ascii_letters + string.octdigits
        token = ""
        token = token.join(random.choice(chars) for i in range (0,13))

        User.user_tokens[token] = (username, name)

        print(User.user_tokens)

        return token
