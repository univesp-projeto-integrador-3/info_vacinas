# project/server/models.py


import datetime

from flask import current_app
from project.server import bcrypt, db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User {0}>".format(self.email)


class Vacina(db.Model):

    __tablename__ = "vacina"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    is_disp_rede_publica = db.Column(db.Boolean, nullable=False, default=False)
    is_disp_clinica_privada = db.Column(
        db.Boolean, nullable=False, default=False)
    is_disp_crie = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, nome, descricao, is_disp_rede_publica, is_disp_clinica_privada, is_disp_crie):
        self.nome = nome
        self.descricao = descricao
        self.is_disp_rede_publica = is_disp_rede_publica
        self.is_disp_clinica_privada = is_disp_clinica_privada
        self.is_disp_crie = is_disp_crie
        self.created_at = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_descricao(self):
        return self.descricao

    def __repr__(self):
        return "<Vacina {0}>".format(self.nome)


class CategoriaIdade(db.Model):

    __tablename__ = "categoria_idade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    periodos_idades = db.relationship(
        'PeriodoIdade', backref='periodo_idade', lazy=True)

    def __init__(self, nome):
        self.nome = nome
        self.created_at = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def __repr__(self):
        return "<CategoriaIdade {0}>".format(self.nome)


class PeriodoIdade(db.Model):

    __tablename__ = "periodo_idade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    categoria_idade = db.Column(db.Integer, db.ForeignKey('categoria_idade.id'),
                                nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao
        self.created_at = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_descricao(self):
        return self.descricao

    def __repr__(self):
        return "<PeriodoIdade {0}>".format(self.nome)
