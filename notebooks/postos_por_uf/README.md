A base de postos de de saúde do Brasil inteiro foi dividida em vários arquivos por UFs, para facilitar o processo de enriquecimento da base, para incluir as informações de localização da UBS.

- AC

  - postos_saude_brasil_AC.csv
    242 de 243 registros mapeados.
- AL

  - postos_saude_brasil_AL.csv
    1060 de 1060 registros mapeados.
- AM

  - postos_saude_brasil_AM.csv
    656
- AP

  - postos_saude_brasil_AP.csv
    198
- BA

  - postos_saude_brasil_BA.csv
    4595
- CE

  - postos_saude_brasil_CE.csv
    2456
- DF

  - postos_saude_brasil_DF.csv
    175 de 175 registros mapeados.
- ES

  - postos_saude_brasil_ES.csv
    915
- GO

  - postos_saude_brasil_GO.csv
    1475
- MA

  - postos_saude_brasil_MA.csv
    2361
- MG

  - postos_saude_brasil_MG.csv
    2833
- MS

  - postos_saude_brasil_MS.csv
    654
- MT

  - postos_saude_brasil_MT.csv
    994
- PA

  - postos_saude_brasil_PA.csv
    2176
- PB

  - postos_saude_brasil_PB.csv
    1645
- PE

  - postos_saude_brasil_PE.csv
    2671
- PI

  - postos_saude_brasil_PI.csv
    1598
- PR

  - postos_saude_brasil_PR.csv
    2647
- RJ

  - postos_saude_brasil_RJ.csv
    1982
- RN

  - postos_saude_brasil_RN.csv
    1315
- RO

  - postos_saude_brasil_RO.csv
    348
- RR

  - postos_saude_brasil_RR.csv
    146
- RS

  - postos_saude_brasil_RS.csv
    2565
- SC

  - postos_saude_brasil_SC.csv
    1851
- SE

  - postos_saude_brasil_SE.csv
    695
- SP

  - postos_saude_brasil_SP.csv
    5134 regsitors, sendo 6 não mapeados

    - LIN JUPIA, REASSENTAMENTO PROJE, CASTILHO, SP, BRASIL
    - VICINAL PREFEITO KOITIRO SATO PBU 010 KM 07 600M, ZONA RURAL, PACAEMBU, SP, BRASIL
    - VICINAL PREFEITO KOITIRO SATO PBU 010 KM 07 6, ZONA RURAL, PACAEMBU, SP, BRASIL
    - ESTRADA MUNICIPAL RIOLANDIA CARDOSO KM 02, ZONA RURAL, RIOLANDIA, SP, BRASIL
    - FAZ SANTA MARINA SETOR II, ZONA RURAL, ROSANA, SP, BRASIL
    - ASSENTAMENTO AGUA SUMIDA, ZONA RURAL, TEODORO SAMPAIO, SP, BRASIL

- TO

  postos_saude_brasil_TO.csv

  433

  O programa usado para incluir a informação de localização das unidades de 
  saúde é o [processa_arquivo_por_uf.py], que pode receber como parâmetro a 
  sigla da UF que se deseja processar.

  Ao final do processo, o arquivo CSV correspondente ao estado desejado será 
  atualizado com as novas informações capturadas. Caso a unidade de saúde já 
  contenha as informações de localização no CSV, o registro é ignorado para 
  capturar informações novamente.



Após o processamento completo do programa processa_arquivo_por_uf.py, 
uma lista com os itens faltando está disponível no arquivo nao_localizados.csv.

Foi passado o programa processa_arquivo_por_uf_extrai_cep.py que extrai o CEP 
dos endereços, e inclui na coluna cep.




## Cadastro Nacional de Estabelecimentos de Saúde
https://cnes.datasus.gov.br/

## Base de dados CENES
http://cnes.datasus.gov.br/pages/downloads/arquivosBaseDados.jsp

## Geonames - The GeoNames geographical database covers all countries 
and contains over eleven million placenames that are available for download 
free of charge.
https://www.geonames.org/

# tratamento de não localizados

 - Cruzar as bases de dados não encontrados (nao_localizados.csv), fazendo a 
ligação com a base de dados de estabelecimentos CNES (cenes_estabelecimentos_202208.csv),
usando como chave o nome fantasia (NO_FANTASIA)

 - A partir desse resultado, fazer o cruzamento com a base Geonames, que possui
 o CPF e dados de endereço 

