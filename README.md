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

Ajuste o arquivo .env e o arquivo *project/server/config.py* com as 
configurações do projeto, e rode:

```sh
$ export APP_NAME="info_vacinas"
$ export APP_SETTINGS=project.server.config.ProductionConfig
$ export FLASK_DEBUG=0
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

## info_vacinas-app-android

Está sendo desenvolvido um App Android para disponibilizar informações sobre 
as unidades de saúde mais próximas do usuário, baseando-se na localização atual 
do usuário.

O repositórido GitHub do APP está disponível em:
https://github.com/univesp-projeto-integrador-3/info_vacinas_app

A pasta ./out contém os arquivos de saída compilados.
