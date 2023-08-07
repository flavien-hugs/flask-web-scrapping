EMAIL = "email@gmail.com"
PASSWORD = "password"


def _create_user(client, addr_email=EMAIL, password=PASSWORD, confirm_password=PASSWORD):
    response = client.post(
        "/auth/register-account/",
        data=dict(addr_email=addr_email, password=password, confirm_password=confirm_password)
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert "Créer votre compte" in data


def _login_user(client, addr_email=EMAIL, password=PASSWORD):
    response = client.post(
        "/auth/login/", data=dict(addr_email=addr_email, password=password),
    )

    assert response.status_code == 200
    data = response.data.decode()
    assert "Se connecter" in data


def _logout_user(client):
    return client.get("/auth/logout/")
    assert response.status_code == 302
    assert response.location == "/auth/login/"
