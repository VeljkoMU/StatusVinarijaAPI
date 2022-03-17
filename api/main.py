from flask import Flask, jsonify
from flask_restful import Api, reqparse
from generatorRouter import Generator
from preditions import Preditions
from userRouter import User
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"*": {"origins": "*"}})

app.logger.info("Server Initiated.")
api.add_resource(Generator, "/generator/<int:genNum>/<string:token>")
api.add_resource(User, "/login/<string:token>")
api.add_resource(Preditions, "/predictions")
app.logger.info("Api resources loaded.")
app.logger.info("Api running.")


if __name__ == "__main__":
    app.run(debug=True)
