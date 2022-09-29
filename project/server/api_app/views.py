# project/server/api_app/views.py
from flask_restx import Api, Resource
from flask import (Blueprint)
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)


@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'hello': 'world'}

    def delete(self):
        return {'hello': 'world'}
