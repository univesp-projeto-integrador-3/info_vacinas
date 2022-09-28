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

for uf in ufs:
    file_path = os.path.join(f'postos_saude_brasil_{uf}.csv')
    df = pd.read_csv(file_path)

    tamanho = len(df)
    print(f'Processando {str(tamanho).zfill(5)} registros')

    df['address'] = df['address'].astype(str)
    df['cep'] = df['address'].str.extract(r'(\d{5}\-?\d{0,4})')

    df.to_csv(file_path, index=False)

    print('Arquivo de saída atualizado com sucesso.', file_path)
