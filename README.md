# info_vacinas

[![.github/workflows/python-package-conda.yml](https://github.com/univesp-projeto-integrador-3/info_vacinas/actions/workflows/python-package-conda.yml/badge.svg?branch=main)](https://github.com/univesp-projeto-integrador-3/info_vacinas/actions/workflows/python-package-conda.yml)

Projeto web para disponibilizar informações sobre vacinas.

O projeto utiliza a linguagem de programação Python com o framework Flask
e banco de dados Postgres e SQL Server.

A aplicação está disponível na internet, no endereço: 
https://info-vacinas.herokuapp.com/

## Clonar o projeto

```sh
$ git clone https://github.com/univesp-projeto-integrador-3/info_vacinas.git
```

## Criar o virtualenv

```sh
$ pip install virtualenv
$ virtualenv info-vacinas
```


## Ativar o virtualenv

### No Windows
```sh
$ .\info-vacinas\Scripts\activate
```

ou 

### No Linux
```sh
$ source ./info-vacinas/bin/activate
```

## Instalar as dependências

```sh
$ pip install -r requirements.txt
```

### Set Environment Variables

Crie um arquivo .env na raiz do projeto com a seguintes chaves e preencha 
de acordo com o seu ambiente:

```.env
APP_NAME="info_vacinas"
APP_SETTINGS=project.server.config.DevelopmentConfig
FLASK_DEBUG=1
SECRET_KEY=SuaSecretKey
DATABASE_URL_SQL_SERVER=mssql+pyodbc://Usuario:Senha@Servidor:Porta/BaseDeDados?driver=ODBC+Driver+17+for+SQL+Server
DATABASE_URL_SQL_SERVER_02=mssql+pyodbc://Usuario:Senha@Servidor:Porta/BaseDeDados?driver=ODBC+Driver+17+for+SQL+Server
API_CEP_URL=https://www.cepaberto.com/api/v3/cep?cep=
API_CEP_TOKEN=TokenDaApiCepAberto
```

By default the app is set to use the production configuration. If you would 
like to use the development configuration, you can alter the `APP_SETTINGS` 
environment variable:

```sh
$ export APP_SETTINGS=project.server.config.DevelopmentConfig
```

### Create DB

```sh
$ python manage.py create-db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create-admin
$ python manage.py create-data
```

### Run the Application

```sh
$ python manage.py run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

Run flake8 on the app:

```sh
$ python manage.py flake
```

or

```sh
$ flake8 project
```

## Query SQL para localizar registros mais próximos

### PostgreSQL

Exemplo, para Latitude = -22.7552899 e Longitude = -47.1570036

select * from (
SELECT  *,( 3959 * acos( cos( radians(-22.7552899) ) * cos( radians( "LATITUDE" ) ) * cos( radians( "LONGITUDE" ) - radians(-47.1570036) ) + sin( radians(-22.7552899) ) * sin( radians( "LATITUDE" ) ) ) ) AS distance 
FROM 
	public.postos_saude_brasil_completo
) al
ORDER by
	distance
LIMIT 20;



## info_vacinas-app-android

Está sendo desenvolvido um App Android para disponibilizar informações sobre 
as unidades de saúde mais próximas do usuário, baseando-se na localização atual 
do usuário.

O repositórido GitHub do APP está disponível em:
https://github.com/univesp-projeto-integrador-3/info_vacinas_app

A pasta ./out contém os arquivos de saída compilados.


A aplicação ficará no ar no heroku na conta gratuita até 28/11/2022.
