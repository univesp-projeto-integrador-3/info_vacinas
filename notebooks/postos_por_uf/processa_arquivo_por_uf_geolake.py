import os
import sys

import pandas as pd
from dotenv import load_dotenv
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Geolake

load_dotenv()  # take environment variables from .env.

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG',
       'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR',
       'RS', 'SC', 'SE', 'SP', 'TO']

if len(sys.argv) > 1:
    ufs = [sys.argv[1].upper()]

print(ufs)


def get_location(row_df):
    # pula os registros que já possuem dados de localização
    if type(row_df['address']) is str:
        return row_df['latitude'], row_df['longitude'], row_df['address'], row_df['point']

    # inicializa a variável que receberá o retorno das APIs de localização
    location = None
    print(' ', row_df['ENDERECO_COMPLETO'])
    try:
        location = geolocator.geocode(query=row_df['ENDERECO_COMPLETO'])
        if not location:
            raise Exception('Sem retorno')
    except Exception as e:
        print(f' Erro: {e}')
        return None, None, None, None

    if not location:
        print(None)
        return None, None, None, None

    print(location.latitude)
    return location.latitude, location.longitude, location.address, location.point


# Geolocators
geolocator = Geolake(
      api_key=os.environ.get('GEOLAKE_API_KEY'), user_agent="info_vacinas")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Cria uma lista com todos os itens não localizados
lista_df_nao_localizados = []
for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'Processando {str(tamanho).zfill(5)} registros')
    df['latitude'], df['longitude'], df['address'], df['point'] = zip(
      *df.apply(get_location, axis=1))

    # remove duplicados
    df.drop_duplicates(inplace=True)
    df.to_csv(file_path, index=False)

    mask = df['latitude'].isna()
    df_nao_localizados = df[mask]
    lista_df_nao_localizados.append(df_nao_localizados)

    print('Arquivo de saída atualizado com sucesso.', file_path)

if len(df_nao_localizados) > 0:
  print('  Arquivo de saída nao_localizados salvo com sucesso.')
  df_nao_localizados = pd.concat(lista_df_nao_localizados)
  df_nao_localizados.to_csv('nao_localizados.csv', index=False)
