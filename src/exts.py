from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

bcrypt = Bcrypt()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
db = SQLAlchemy(metadata=metadata)
cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300})

# login_manager.login_view = "auth_bp.login"
login_manager.session_protection = "strong"
login_manager.login_message_category = "dander"
login_manager.needs_refresh_message_category = "dander"
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.needs_refresh_message = "Pour protéger votre compte,\
    veuillez vous réauthentifier pour accéder à cette page."
