import logging as lg
import os

from flask_migrate import Migrate
from flask_migrate import upgrade
from src import create_yimba_app
from src.exts import db
from src.services.account import Project
from src.services.account import User


yimba_app = create_yimba_app(os.environ.get("FLASK_CONFIG"))
migrate = Migrate(yimba_app, db, render_as_batch=True)


@yimba_app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        users=User,
        projects=Project,
    )


@yimba_app.cli.command("init_db")
def init_db():
    upgrade()
    db.create_all()
    db.session.commit()
    User.insert_default_user()
    lg.info("Database initialized !")


if __name__ == "__main__":
    yimba_app.run(host=os.environ.get("APP_HOST"))
