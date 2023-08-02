import logging
import os
from logging.handlers import RotatingFileHandler

from config import config
from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from src import exts


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
        from src.services.account.routes import auth_bp, project_bp
        from src.services.dashboard.routes import dashboard_bp

        yimba_app.register_blueprint(auth_bp)
        yimba_app.register_blueprint(project_bp)
        yimba_app.register_blueprint(dashboard_bp)

        @yimba_app.route("/")
        def entrypoint():
            return redirect(url_for("auth_bp.login"))

        @yimba_app.errorhandler(400)
        def key_error(e):
            page_title = e.name
            return (
                render_template(
                    "page/error.html",
                    page_title=page_title,
                    error=e,
                ),
                400,
            )

        @yimba_app.errorhandler(403)
        def forbidden(e):
            page_title = f"erreur {e}"
            return (
                render_template(
                    "page/error.html",
                    page_title=page_title,
                    error=e,
                ),
                403,
            )

        @yimba_app.errorhandler(404)
        def page_not_found(e):
            page_title = e.name
            return (
                render_template(
                    "page/error.html",
                    page_title=page_title,
                    error=e,
                ),
                404,
            )

        @yimba_app.errorhandler(500)
        def internal_server_error(e):
            page_title = e.name
            return (
                render_template(
                    "page/error.html",
                    page_title=page_title,
                    error=e,
                ),
                500,
            )

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
