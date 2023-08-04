import uuid
from datetime import datetime

from src.exts import db


class CRUDMixin(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(
        db.Integer,
        unique=True,
        index=True,
        nullable=False,
        primary_key=True,
    )
    public_id = db.Column(
        db.String(40), unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.utcnow(), default=datetime.utcnow()
    )

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)
        return self.save()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def remove(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def disable(self):
        self.is_active = False
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, (int, int)), isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    @classmethod
    def all(cls):
        return cls.query.all()
