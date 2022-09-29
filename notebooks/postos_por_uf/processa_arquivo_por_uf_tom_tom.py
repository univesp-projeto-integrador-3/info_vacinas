import os
import sys

import pandas as pd
from dotenv import load_dotenv
from geopy.geocoders import TomTom

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


def get_location_tomtom(api_key_env, endereco_completo):
    api_key = os.environ.get(api_key_env)
    geolocator = TomTom(api_key=api_key, user_agent="info_vacinas")
    try:
        location = geolocator.geocode(endereco_completo)
    except Exception as e:
        raise Exception("Nenhum retorno na API TomTom", api_key_env, e)
    if not location:
        raise Exception("Nenhum retorno na API TomTom", api_key_env)
    return location


def get_location(row_df):
    # pula os registros que já possuem dados de localização
    if type(row_df['address']) is str:
        return row_df['latitude'], row_df['longitude'], row_df['address'], row_df['point']

    # inicializa a variável que receberá o retorno das APIs de localização
    location = None
    endereco_completo = row_df['ENDERECO_COMPLETO']
    print(' ', endereco_completo)
    try:
        location = get_location_tomtom('TOMTOM_API_KEY_20', endereco_completo)
    except Exception as e:
        try:
            location = get_location_tomtom(
              'TOMTOM_API_KEY_19', endereco_completo)
        except Exception as e:
            try:
                location = get_location_tomtom(
                  'TOMTOM_API_KEY_18', endereco_completo, e)
            except Exception as e:
                try:
                    location = get_location_tomtom(
                      'TOMTOM_API_KEY_17', endereco_completo, e)
                except Exception as e:
                    try:
                        location = get_location_tomtom(
                          'TOMTOM_API_KEY_16', endereco_completo, e)
                    except Exception as e:
                        try:
                            location = get_location_tomtom(
                              'TOMTOM_API_KEY_15', endereco_completo, e)
                        except Exception as e:
                            try:
                                location = get_location_tomtom(
                                  'TOMTOM_API_KEY_14', endereco_completo, e)
                            except Exception as e:
                                try:
                                    location = get_location_tomtom(
                                      'TOMTOM_API_KEY_13', endereco_completo, e)
                                except Exception as e:
                                    try:
                                        location = get_location_tomtom(
                                          'TOMTOM_API_KEY_12',
                                          endereco_completo, e)
                                    except Exception as e:
                                        try:
                                            location = get_location_tomtom(
                                              'TOMTOM_API_KEY_11',
                                              endereco_completo, e)
                                        except Exception as e:
                                            print(f' Erro: {e}')
                                            location = None

    if not location:
        print(None)
        return None, None, None, None

    print(location.latitude)
    return location.latitude, location.longitude, location.address, location.point


# Cria uma lista com todos os itens não localizados
lista_df_nao_localizados = []
for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'Processando {str(tamanho).zfill(5)} registros')
    df['latitude'], df['longitude'], df['address'], df['point'] = zip(
      *df.apply(get_location, axis=1))

    df.to_csv(file_path, index=False)

    mask = df['latitude'].isna()
    df_nao_localizados = df[mask]
    lista_df_nao_localizados.append(df_nao_localizados)

    print('Arquivo de saída atualizado com sucesso.', file_path)

df_nao_localizados = pd.concat(lista_df_nao_localizados)
df_nao_localizados.to_csv('nao_localizados.csv', index=False)
