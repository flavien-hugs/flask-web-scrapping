import sys

import pytest
from flask import current_app
from src import create_yimba_app
from src.exts import db

sys.path.append("..")


@pytest.fixture
def app():
    app = create_yimba_app("test")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_app_exists(client):
    assert current_app is not None


def test_app_is_testing(client):
    assert app.config["TESTING"] is True
