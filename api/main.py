from flask import Flask, jsonify
from flask_restful import Api, reqparse
from generatorRouter import Generator
from userRouter import User

app = Flask(__name__)
api = Api(app)


api.add_resource(Generator, "/generator/<int:genNum>")
api.add_resource(User, "/login")


if __name__ == "__main__":
    app.run(debug=True)
