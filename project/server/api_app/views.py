# project/server/api_app/views.py
from flask_restx import Api, Resource
from flask import (Blueprint)
from flask_restx import reqparse
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)


parser = reqparse.RequestParser()
parser.add_argument(
    'latitude',
    type=float,
    required=True,
    help="Latitude não pode ser vazio!",
    location='args')
parser.add_argument(
    'longitude',
    type=float,
    required=True,
    help="Longitude não pode ser vazio!",
    location='args')
parser.add_argument(
    'quantidade',
    type=int,
    required=True,
    help="Quantidade não pode ser vazio!",
    location='args')


@api.route(
  "/unidades_saude")
class UnidadesSaude(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()

        args['latitude']
        args['longitude']
        args['quantidade']

        lista_unidades_saude = []
        unidade = {
          'CO_CNES': '253699',
          'NOME': 'UBS SEM TUPIUTUBA',
          'LOGRADOURO': 'RUA MARA SILVA',
          'NUMERO': '25',
          'BAIRRO': 'VILA FORMOSA',
          'MUNICIPIO': 'SAO PAULO',
          'UF': 'SP',
          'LATITUDE': -25.3623,
          'LONGITUDE': 69.3632,
          'CEP': '03382-130',
        }
        lista_unidades_saude.append(unidade)
        unidade = {
          'CO_CNES': '253699',
          'NOME': 'UBS SEM TUPIUTUBA',
          'LOGRADOURO': 'RUA MARA SILVA',
          'NUMERO': '25',
          'BAIRRO': 'VILA FORMOSA',
          'MUNICIPIO': 'SAO PAULO',
          'UF': 'SP',
          'LATITUDE': -25.3623,
          'LONGITUDE': 69.3632,
          'CEP': '03382-130',
        }
        lista_unidades_saude.append(unidade)
        unidade = {
          'CO_CNES': '253699',
          'NOME': 'UBS SEM TUPIUTUBA',
          'LOGRADOURO': 'RUA MARA SILVA',
          'NUMERO': '25',
          'BAIRRO': 'VILA FORMOSA',
          'MUNICIPIO': 'SAO PAULO',
          'UF': 'SP',
          'LATITUDE': -25.3623,
          'LONGITUDE': 69.3632,
          'CEP': '03382-130',
        }
        lista_unidades_saude.append(unidade)
        unidade = {
          'CO_CNES': '253699',
          'NOME': 'UBS SEM TUPIUTUBA',
          'LOGRADOURO': 'RUA MARA SILVA',
          'NUMERO': '25',
          'BAIRRO': 'VILA FORMOSA',
          'MUNICIPIO': 'SAO PAULO',
          'UF': 'SP',
          'LATITUDE': -25.3623,
          'LONGITUDE': 69.3632,
          'CEP': '03382-130',
        }
        lista_unidades_saude.append(unidade)

        return {"resultado": lista_unidades_saude}
