from tests import utils
from flask_login import current_user
from src.services.account import User


def test_get_entrypoint(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.location == "/auth/login/"


def test_register_user_success(client):
    utils._create_user(client)


def test_login_user_success(client):
    utils._create_user(client, "email@gmail.com", "password", "password")
    utils._login_user(client, "email@gmail.com", "password")
    response = client.get("/panel/")
    assert response.status_code == 302


def test_logout_redirects_to_login(client):
    utils._logout_user(client)
