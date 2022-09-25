import os
import sys

import pandas as pd
from dotenv import load_dotenv
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import HereV7, Nominatim, TomTom

load_dotenv()  # take environment variables from .env.

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG',
       'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR',
       'RS']

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
        # tenta fazer a localização usando o Nominatim
        print(' Here')
        location = geolocator_here.geocode(row_df['ENDERECO_COMPLETO'])
        if not location:
            raise Exception('Sem retorno')
    except Exception as e:
        print(f' Erro: {e}')
        return None, None, None, None

    if not location:
        return None, None, None, None

    return location.latitude, location.longitude, location.address, location.point


# Geolocators
geolocator_nominatim = Nominatim(user_agent="info_vacinas")
geolocator_tomtom = TomTom(
      api_key='wvuAFmBut64DLjQqey19XtfuMXZilzbj', user_agent="info_vacinas")
geolocator_here = HereV7(
      apikey=os.environ.get('HERE_API_KEY'), user_agent="info_vacinas")
geocode_nominatim = RateLimiter(
  geolocator_nominatim.geocode, min_delay_seconds=0.25)
geocode_tomtom = RateLimiter(geolocator_tomtom.geocode, min_delay_seconds=0.25)
geocode_here = RateLimiter(geolocator_here.geocode, min_delay_seconds=0.25)

for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'Processando {str(tamanho).zfill(5)} registros')
    df['latitude'], df['longitude'], df['address'], df['point'] = zip(
      *df.apply(get_location, axis=1))

    df.to_csv(file_path, index=False)
    print('Arquivo de saída atualizado com sucesso.', file_path)
