# project/server/api/views.py
import os
from datetime import datetime

import requests
from flask_restx import Api
import unidecode
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from flask import (Blueprint, Markup, flash, jsonify, redirect,
                   render_template, request, url_for)
from project.server import db, api
from project.server.main.forms import ConsultaCalendarioForm, ConsultaUbsForm
from project.server.models import Template
from flask_restx import Resource

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
