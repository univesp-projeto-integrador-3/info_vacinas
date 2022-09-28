# Tratamento de Bases de Dados - UBS

A base de postos de de saúde do Brasil inteiro foi dividida em vários arquivos 
por UFs, para facilitar o processo de enriquecimento da base, para incluir as 
informações de localização das UBSs.

Para pegar a localização das unidades foi utilizada a biblioteca Python 
[geopy](https://geopy.readthedocs.io/en/stable/), que acessa diversas APIs
de localização. Fizemos o processo em passos, cada um com a sua API:

# Tratamento de dados

## 1º Passo
Foi processado usando [Nominatim - Open-source with OpenStreetMap data]
(https://nominatim.org/)
processa_arquivo_por_uf_nominatim.py

## 2º Passo
Os registros não localizados até o momento foram reprocessados usando o serviço
de geolocalização do [TomTom API](https://developer.tomtom.com/search-api/documentation/product-information/introduction).
processa_arquivo_por_uf_tom_tom.py

## 3º Passo
Os registros não localizados até o momento foram reprocessados usando o serviço
de geolocalização do [Here API](https://developer.here.com/documentation/geocoding-search-api/dev_guide/index.html).
Até esse momento, ainda restavam 36 de 42.807 registros.
processa_arquivo_por_uf_here.py

## 4º Passo
Os registros não localizados até o momento foram reprocessados usando o serviço
de geolocalização do [GeoLake](https://geolake.com/).
Após esse momento, todos os registors foram localizados, sendo processados um
total de 42.807 registros.
processa_arquivo_por_uf_geolake.py

## 5º Passo

Foi criada uma nova coluna para inserir o cep da unidade de saúde, aplicando 
para isso uma expressão regular que extrai o CEP do endereço completo retornado
pelo provedor de serviço de geolocalização realizados nos passos anteriores.

O mesmo programa também foi utilizado para inserir a coluna com o código CNES, 
que será utilizado como identificador único da UBS.

## 6º Passo
Depois de processados os passos acima, alguns registros ficaram duplicados, 
então foi processado o programa abaixo para remover as duplicidades de UBSs.
processa_arquivo_por_uf_remove_duplicados.py

## 7º Passo
Unifica todos os arquivos em um único arquivo, que será importado para o banco
de dados da aplicação.
processa_arquivo_por_uf_unifica_arquivo.py

## Resumo dos dados

- AC
  - postos_saude_brasil_AC.csv
- AL
  - postos_saude_brasil_AL.csv
- AM
  - postos_saude_brasil_AM.csv
- AP
  - postos_saude_brasil_AP.csv
- BA
  - postos_saude_brasil_BA.csv
- CE
  - postos_saude_brasil_CE.csv
- DF
  - postos_saude_brasil_DF.csv
- ES
  - postos_saude_brasil_ES.csv
- GO
  - postos_saude_brasil_GO.csv
- MA
  - postos_saude_brasil_MA.csv
- MG
  - postos_saude_brasil_MG.csv
- MS
  - postos_saude_brasil_MS.csv
- MT
  - postos_saude_brasil_MT.csv
- PA
  - postos_saude_brasil_PA.csv
- PB
  - postos_saude_brasil_PB.csv
- PE
  - postos_saude_brasil_PE.csv
- PI
  - postos_saude_brasil_PI.csv
- PR
  - postos_saude_brasil_PR.csv
- RJ
  - postos_saude_brasil_RJ.csv
- RN
  - postos_saude_brasil_RN.csv
- RO
  - postos_saude_brasil_RO.csv
- RR
  - postos_saude_brasil_RR.csv
- RS
  - postos_saude_brasil_RS.csv
- SC
  - postos_saude_brasil_SC.csv
- SE
  - postos_saude_brasil_SE.csv
- SP
  - postos_saude_brasil_SP.csv
- TO
  - postos_saude_brasil_TO.csv

AC - 243 registros
AL - 1055 registros
AM - 650 registros
AP - 198 registros
BA - 4437 registros
CE - 2384 registros
DF - 175 registros
ES - 909 registros
GO - 1465 registros
MA - 2312 registros
MG - 5610 registros
MS - 649 registros
MT - 980 registros
PA - 2125 registros
PB - 1629 registros
PE - 2596 registros
PI - 1575 registros
PR - 2528 registros
RJ - 1961 registros
RN - 1287 registros
RO - 347 registros
RR - 146 registros
RS - 2468 registros
SC - 1766 registros
SE - 695 registros
SP - 5063 registros
TO - 430 registros


TO - 430 registros
Salvando arquivo postos_saude_brasil_completo.csv
45683 registros

# Dados utilizados

## Cadastro Nacional de Estabelecimentos de Saúde
https://cnes.datasus.gov.br/

## Base de dados CENES
http://cnes.datasus.gov.br/pages/downloads/arquivosBaseDados.jsp

## Geonames - The GeoNames geographical database covers all countries 
and contains over eleven million placenames that are available for download 
free of charge.
https://www.geonames.org/

# tratamento de não localizados

Não houve a necessidade de se realizar o tratamento de não localizados, pois
todos os registros foram retornados com sucesso.

Caso necessário, as etapas seriam as seguintes:

 - Cruzar as bases de dados não encontrados (nao_localizados.csv), fazendo a 
ligação com a base de dados de estabelecimentos CNES (cenes_estabelecimentos_202208.csv),
usando como chave o nome fantasia (CO_CNES)

 - A partir desse resultado, fazer o cruzamento com a base Geonames, que possui
 o CEF e dados de endereço 
