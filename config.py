import os

from dotenv import dotenv_values

env = dotenv_values(".flaskenv")


class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SITE_NAME = "Yimba"

    SECRET_KEY = env.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URL")

    RESTX_VALIDATE = True

    API_BASE_URL: str = env.get("API_BASE_URL")
    API_ACCESS_TOKEN: str = env.get("API_ACCESS_TOKEN")

    @staticmethod
    def init_app(yimba_app):
        pass


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdConfig(Config):
    @classmethod
    def init_app(cls, yimba_app):
        Config.init_app(yimba_app)
        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        yimba_app.logger.addHandler(syslog_handler)


config = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
