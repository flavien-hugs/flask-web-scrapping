from datetime import datetime

from flask import flash
from flask import redirect
from flask import url_for
from flask_login import current_user
from flask_login import UserMixin
from src.exts import bcrypt
from src.exts import db
from src.exts import login_manager
from src.services.commun import CRUDMixin


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = "user"

    addr_email = db.Column(db.String(180), nullable=True, unique=True)
    password_hash = db.Column(db.String(100), unique=True, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.addr_email

    def __repr__(self):
        return f"User({self.public_id}, {self.addr_email})"

    @classmethod
    def find_by_email(cls, addr_email):
        return cls.query.filter_by(addr_email=addr_email).first()

    @classmethod
    def insert_default_user(cls):
        from dotenv import dotenv_values

        env = dotenv_values(".flaskenv")

        email = env.get("DEFAULT_USER")
        password = env.get("DEFAULT_PASSWORD")
        password_hash = password
        user = cls(addr_email=email)
        user.set_password(password_hash)
        user.save()


class Project(CRUDMixin, db.Model):
    __tablename__ = "project"
    updated_at = None
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.public_id"), nullable=False)
    user = db.relationship("User", backref="user_project")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Project({self.public_id}, {self.name}"

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, user=current_user).first()

    @classmethod
    def find(cls):
        return (
            cls.query.filter_by(user=current_user).order_by(cls.created_at.desc()).all()
        )


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("Vous devez être connecté pour voir cette page.")
    return redirect(url_for("auth_bp.login"))
