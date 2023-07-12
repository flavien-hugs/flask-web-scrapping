import logging as lg

from flask_migrate import Migrate
from flask_migrate import upgrade

from src.exts import db
from src import create_yimba_app
from dotenv import dotenv_values

env = dotenv_values(".flaskenv")


yimba_app = create_yimba_app(env.get("FLASK_CONFIG"))
migrate = Migrate(yimba_app, db, render_as_batch=True)


@yimba_app.cli.command("init_db")
def init_db():
    upgrade()
    db.create_all()
    db.session.commit()
    lg.warning("Database initialized !")


@yimba_app.shell_context_processor
def make_shell_context():
    return dict(
        db=db
    )


if __name__ == "__main__":
    yimba_app.run(host='0.0.0.0')
