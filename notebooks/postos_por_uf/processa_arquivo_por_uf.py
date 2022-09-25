import os
import sys

import pandas as pd
import numpy as np
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

if (len(sys.argv) > 1):
    ufs = [sys.argv[1].upper()]

print(ufs)

# Geolocators
geolocator_nominatim = Nominatim(user_agent="info_vacinas")
geolocator_tomtom = TomTom(
      api_key='wvuAFmBut64DLjQqey19XtfuMXZilzbj', user_agent="info_vacinas")
geolocator_here = HereV7(
      apikey=os.environ.get('HERE_API_KEY'), user_agent="info_vacinas")
geocode_nominatim = RateLimiter(
  geolocator_nominatim.geocode, min_delay_seconds=0)
geocode_tomtom = RateLimiter(geolocator_tomtom.geocode, min_delay_seconds=0)
geocode_here = RateLimiter(geolocator_here.geocode, min_delay_seconds=0)

for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)

    print(f'Processando {str(tamanho).zfill(5)} registros')
    # for index, row in df[::-1].iterrows():
    for index, row in df.iterrows():
        # pula os registros que já possuem dados de localização
        if type(row['address']) is str:
            continue

        print(
          f'Processando {str(index+1).zfill(5)} de {str(tamanho).zfill(5)}'
        )

        # inicializa a variável que receberá o retorno das APIs de localização
        location = None

        try:
            # tenta fazer a localização usando o Nominatim
            location = geolocator_nominatim.geocode(row['ENDERECO_COMPLETO'])
        except Exception as e:
            print(f'Erro: {e}')
            # se a localização não retorna nada, tenta usar o TomTom
            try:
                location = geolocator_tomtom.geocode(row['ENDERECO_COMPLETO'])
            except Exception as e:
                # se a localização não retorna nada, tenta usar o Here
                print(f'Erro: {e}')
                try:
                    location = geolocator_here.geocode(row['ENDERECO_COMPLETO'])
                except Exception as e:
                    # salva o CSV com os dados buscados até aquele momento
                    df.to_csv(file_path, index=False)
                    if not location:
                        continue

        # se em nenhuma das três tentativas conseguiu retornar a localização, 
        # vai para o próximo registro
        if not location:
            continue

        print(location)

        # salva de 10 em 10 registros o arquivo de saída
        if index%10 == 0:
            df.to_csv(file_path, index=False)

        row['latitude'] = location.latitude
        row['longitude'] = location.longitude
        row['address'] = location.address
        row['point'] = location.point

    df.to_csv(file_path, index=False)
    print('Arquivo de saída atualizado com sucesso.', file_path)
