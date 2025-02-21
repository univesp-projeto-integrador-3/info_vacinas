# project/server/models.py
import datetime

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import URLSafeSerializer as Serializer
from project.server import bcrypt, db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash


class Template(db.Model):
    __tablename__ = "template"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    caminho = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, caminho):
        self.nome = nome
        self.caminho = caminho

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_caminho(self):
        return self.caminho

    def __repr__(self):
        return "<Template {0}>".format(self.caminho)


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

    def __init__(
      self,
      nome,
      descricao,
      is_disp_rede_publica,
      is_disp_clinica_privada,
      is_disp_crie
      ):
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
    categoria_idade = db.Column(
      db.Integer,
      db.ForeignKey('categoria_idade.id'),
      nullable=False
    )

    def __init__(self, descricao):
        self.descricao = descricao
        self.created_at = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_descricao(self):
        return self.descricao

    def __repr__(self):
        return "<PeriodoIdade {0}>".format(self.nome)


class EditableHTML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    editor_name = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)

    @staticmethod
    def get_editable_html(editor_name):
        editable_html_obj = EditableHTML.query.filter_by(
            editor_name=editor_name).first()

        if editable_html_obj is None:
            editable_html_obj = EditableHTML(editor_name=editor_name, value='')
        return editable_html_obj


class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('UserOld', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class UserOld(UserMixin, db.Model):
    __tablename__ = 'users_old'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from random import choice, seed

        from faker import Faker
        from sqlalchemy.exc import IntegrityError

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='password',
                confirmed=True,
                role=choice(roles),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UnidadeSaude(db.Model):

    __tablename__ = "postos_saude_brasil_completo"

    co_cnes = db.Column('CO_CNES', db.Integer, autoincrement=False)
    nome = db.Column(
      'NOME', db.String(255), nullable=False, primary_key=True)
    uf = db.Column('UF', db.String(2), nullable=False)
    municipio = db.Column(
      'MUNICIPIO', db.String(255), unique=False, nullable=True)
    logradouro = db.Column(
      'LOGRADOURO', db.String(255), unique=False, nullable=True)
    numero = db.Column('NUMERO', db.String(255), unique=False, nullable=True)
    bairro = db.Column('BAIRRO', db.String(255), unique=False, nullable=True)
    endreco_completo = db.Column(
      'ENDERECO_COMPLETO', db.String(255), unique=False, nullable=True)
    latitude = db.Column('LATITUDE', db.Float, autoincrement=False)
    longitude = db.Column('LONGITUDE', db.Float, autoincrement=False)
    endereco_api = db.Column(
      'ENDERECO_API', db.String(255), unique=False, nullable=True)
    point = db.Column('POINT', db.String(255), unique=False, nullable=True)
    cep = db.Column('CEP', db.String(255), unique=False, nullable=True)

    def __init__(
      self,
      co_cnes,
      nome,
      uf,
      municipio,
      logradouro,
      numero,
      bairro,
      endereco_completo,
      latitude,
      longitude,
      endereco_api,
      point,
      cep
      ):
        self.co_cnes = co_cnes
        self.nome = nome
        self.uf = uf
        self.municipio = municipio
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.endereco_completo = endereco_completo
        self.latitude = latitude
        self.longitude = longitude
        self.endereco_api = endereco_api
        self.point = point
        self.cep = cep

    def get_co_cnes(self):
        return self.co_cnes

    def get_nome(self):
        return self.nome

    def get_uf(self):
        return self.uf

    def get_municipio(self):
        return self.municipio

    def get_logradouro(self):
        return self.logradouro

    def get_numero(self):
        return self.numero

    def get_bairro(self):
        return self.bairro

    def get_endereco_completo(self):
        return self.endreco_completo

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_endereco_api(self):
        return self.endereco_api

    def get_point(self):
        return self.point

    def get_cep(self):
        return self.cep

    def __repr__(self):
        return f"<UnidadeSaude {self.nome} - {self.endreco_completo}>"
