# project/server/config.py

import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv("APP_NAME", "info_vacinas")
    BCRYPT_LOG_ROUNDS = 4
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL_SQL_SERVER",
        "sqlite:///{0}".format(os.path.join(basedir, "dev.db"))
    )
    SQLALCHEMY_DATABASE_URI_02 = os.environ.get(
        "DATABASE_URL_SQL_SERVER_02",
        "sqlite:///{0}".format(os.path.join(basedir, "dev.db"))
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_TEST_URL",
        "sqlite:///"
    )
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL_SQL_SERVER",
        "sqlite:///{0}".format(os.path.join(basedir, "prod.db")),
    )
    SQLALCHEMY_DATABASE_URI_02 = os.environ.get(
        "DATABASE_URL_SQL_SERVER_02",
        "sqlite:///{0}".format(os.path.join(basedir, "dev.db"))
    )    
    WTF_CSRF_ENABLED = True
