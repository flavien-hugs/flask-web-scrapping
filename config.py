import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SITE_NAME = "Yimba"

    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(
        BASE_DIR, "dev.sqlite3"
    )

    RESTX_VALIDATE = True

    API_BASE_URL = os.environ.get("API_BASE_URL")
    API_ACCESS_TOKEN = os.environ.get("API_ACCESS_TOKEN")

    @staticmethod
    def init_app(yimba_app):
        pass


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TEMPLATES_AUTO_RELOAD = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


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
