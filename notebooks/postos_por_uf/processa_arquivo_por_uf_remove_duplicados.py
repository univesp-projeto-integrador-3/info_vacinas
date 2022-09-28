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


# Cria uma lista com todos os itens não localizados
lista_df_nao_localizados = []
for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'Processando {str(tamanho).zfill(5)} registros')

    # remove duplicados
    print('Remove duplicados')
    print(f'{str(len(df)).zfill(5)}')
    df.drop_duplicates(inplace=True)

    colunas = df.columns

    if 'NOME' in colunas:
        df.drop_duplicates(subset='NOME', keep="first", inplace=True)

    if 'ESTABELECIMENTO' in colunas:
        df.drop_duplicates(subset='ESTABELECIMENTO', keep="first", inplace=True)

    print(f'{str(len(df)).zfill(5)}')

    print('Salvando arquivo', file_path)
    df.to_csv(file_path, index=False)
