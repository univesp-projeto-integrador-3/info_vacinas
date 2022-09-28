import os
import sys

import pandas as pd
from dotenv import load_dotenv

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
lista_dfs = []
for uf in ufs:
    print(uf, '-', end=' ')
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'{str(tamanho)} registros')

    # ajusta ordem das colunas
    df = df[[
      'CO_CNES',
      'NOME',
      'LOGRADOURO',
      'NUMERO',
      'BAIRRO',
      'MUNICIPIO',
      'UF',
      'CEP',
      'ENDERECO_COMPLETO',
      'LATITUDE',
      'LONGITUDE',
      'ENDERECO_API',
      'POINT',
    ]]

    lista_dfs.append(df)


file_path_saida = os.path.join('postos_saude_brasil_completo.csv')
df_saida = pd.concat(lista_dfs)
print('Salvando arquivo', file_path_saida)
tamanho = len(df_saida)
print(f'{str(tamanho)} registros')
df_saida.to_csv(file_path_saida, index=False)
