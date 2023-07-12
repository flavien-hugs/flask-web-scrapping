import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import jsonify

from src import exts
from config import config


def create_yimba_app(config_name):
    yimba_app = Flask(__name__, instance_relative_config=True)
    yimba_app.config.from_object(config[config_name])
    config[config_name].init_app(yimba_app)

    yimba_app.url_map.strict_slashes = False

    exts.ma.init_app(yimba_app)
    exts.db.init_app(yimba_app)
    exts.bcrypt.init_app(yimba_app)
    exts.login_manager.init_app(yimba_app)
    exts.migrate.init_app(yimba_app, exts.db)
    exts.cors.init_app(yimba_app, origins="*", supports_credentials=True)

    with yimba_app.app_context():

        @yimba_app.before_request
        def log_entry():
            yimba_app.logger.debug("Demande de traitement")

        @yimba_app.teardown_request
        def log_exit(exc):
            yimba_app.logger.debug("Traitement de la demande terminé", exc_info=exc)

        if not yimba_app.debug:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/logging.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)

            yimba_app.logger.addHandler(file_handler)
            yimba_app.logger.setLevel(logging.INFO)
            yimba_app.logger.info("running oncoflow app")

        return yimba_app
