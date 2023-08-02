import secrets
from datetime import datetime

from flask import flash, redirect, url_for

from flask_login import UserMixin
from src.services.commun import CRUDMixin
from src.exts import db, bcrypt, login_manager



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
        user = cls(addr_email="yimba@yimba.com")
        password_hash = "yimba"
        user.set_password(password_hash)
        user.save()


class Project(CRUDMixin, db.Model):

    __tablename__ = "project"
    updated_at = None
    name = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.public_id"), nullable=False)
    user = db.relationship("User", backref="user_project")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Project({self.public_id}, {self.name}"

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find(cls):
        return cls.query.order_by(cls.created_at.desc()).all()



@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("Vous devez être connecté pour voir cette page.")
    return redirect(url_for("auth_bp.login"))
