# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv("APP_NAME", "FoCo DS Portal")
    BCRYPT_LOG_ROUNDS = 4
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGODB_DB")
    MONGO_HOST = os.getenv("MONGODB_HOST")
    MONGO_PORT = os.getenv("MONGODB_PORT")
    TWTR_CONSUMER_KEY = os.getenv("TWTR_CONSUMER_KEY")
    TWTR_CONSUMER_SECRET = os.getenv("TWTR_CONSUMER_SECRET")
    TWTR_TOKEN_KEY = os.getenv("TWTR_TOKEN_KEY")
    TWTR_TOKEN_SECRET = os.getenv("TWTR_TOKEN_SECRET")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///{0}".format(os.path.join(basedir, "dev.db"))
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL", "sqlite:///")
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    WTF_CSRF_ENABLED = True
