# project/server/api_app/views.py
from flask_restx import Api, Resource, reqparse, cors
from flask import (Blueprint)
import os
import requests
from dotenv import load_dotenv
from project.server import db
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


parser_cep = reqparse.RequestParser()
parser_cep.add_argument(
    'cep',
    type=str,
    required=True,
    help="CEP não pode ser vazio!",
    location='args'
)


def get_unidades_by_latitude_longitude(latitude, longitude, uf):
    sql = f'''
        SELECT DISTINCT TOP 10
             CO_CNES
            ,NOME
            ,LOGRADOURO
            ,NUMERO
            ,BAIRRO
            ,MUNICIPIO
            ,UF
            ,CEP
            ,LATITUDE
            ,LONGITUDE
            ,sqrt(square(abs(LATITUDE-({latitude}))) +
            square(abs(LONGITUDE-({longitude})))) as DISTANCIA
        FROM
            [univesp].[dbo].[postos_saude_brasil_completo]
        WHERE
            sqrt(square(abs(LATITUDE-({latitude}))) +
            square(abs(LONGITUDE-({longitude})))) < 50
        ORDER BY
            DISTANCIA
        ASC
        '''

    # desabilita temporariamente o uso do recurso UF, para permitir mostrar
    # aos membros do grupo as inconsistências na base de dados
    if uf:
        sql2 = f'''
            SELECT DISTINCT TOP 10
                CO_CNES
                ,NOME
                ,LOGRADOURO
                ,NUMERO
                ,BAIRRO
                ,MUNICIPIO
                ,UF
                ,CEP
                ,LATITUDE
                ,LONGITUDE
                ,sqrt(square(abs(LATITUDE-({latitude}))) +
                square(abs(LONGITUDE-({longitude})))) as DISTANCIA
            FROM
                [univesp].[dbo].[postos_saude_brasil_completo]
            WHERE
                sqrt(square(abs(LATITUDE-({latitude}))) +
                square(abs(LONGITUDE-({longitude})))) < 50 AND UF = '{uf}'
            ORDER BY
                DISTANCIA
            ASC
            '''
        print(sql2)

    rows = []
    try:
        rows = db.engine.execute(sql)
    except Exception as e:
        print('Erro executando sql', sql, e)

    lista_unidades_saude = [dict(row) for row in rows]
    return lista_unidades_saude


@api.route(
  "/unidades_saude/consulta_por_localizacao")
class UnidadesSaude(Resource):
    @api.expect(parser)
    @cors.crossdomain(origin="*")
    def get(self):
        args = parser.parse_args()

        lista_unidades_saude = get_unidades_by_latitude_longitude(
            args['latitude'], args['longitude'], None)

        return {"resultado": lista_unidades_saude}


@api.route(
  "/unidades_saude/consulta_por_cep")
class UnidadesSaude(Resource):
    @api.expect(parser_cep)
    @cors.crossdomain(origin="*")
    def get(self):
        args = parser_cep.parse_args()

        cep = str(args['cep'])

        print('O cep digitado foi', cep)
        # monta a url para consulta dos dados do cep na API
        url = os.environ.get("API_CEP_URL")+cep.replace("-", "")

        headers = {
            'Authorization': 'Token token=' + os.environ.get("API_CEP_TOKEN")}
        response = requests.get(url, headers=headers)

        lista_unidades_saude = []

        if response.status_code == 200:
            dados_cep = response.json()
            print(dados_cep)
            uf = dados_cep.get('estado').get('sigla').upper()

            lista_unidades_saude = get_unidades_by_latitude_longitude(
                dados_cep['latitude'], dados_cep['longitude'], uf)

        return {"resultado": lista_unidades_saude}
