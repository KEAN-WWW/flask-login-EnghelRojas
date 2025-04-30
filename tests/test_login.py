import pytest
from flask import url_for
from application.database.models import User
from application import init_app, db

@pytest.fixture(name="app")
def create_app():
    app = init_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app

@pytest.fixture(name="client")
def create_client(app):
    with app.test_client() as client:
        yield client

def test_user_invalid_login(client):
    response = client.post("/login", data={"email": "wrong@email.com", "password": "wrong"}, follow_redirects=True)
    assert b"User Not Found" in response.data

def test_user_login(client, app):
    with app.app_context():
        user = User.create("steve@123.com", "123456")
        db.session.add(user)
        db.session.commit()
    response = client.post("/login", data={"email": "steve@123.com", "password": "123456"}, follow_redirects=True)
    assert b"Welcome, steve@123.com" in response.data

def test_user_invalid_passwd(client, app):
    with app.app_context():
        user = User.create("steve@123.com", "123456")
        db.session.add(user)
        db.session.commit()
    response = client.post("/login", data={"email": "steve@123.com", "password": "wrong"}, follow_redirects=True)
    assert b"Password Incorrect" in response.data

def test_user_logout(client, app):
    with app.app_context():
        user = User.create("steve@123.com", "123456")
        db.session.add(user)
        db.session.commit()
    client.post("/login", data={"email": "steve@123.com", "password": "123456"}, follow_redirects=True)
    response = client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data

def test_user_access_no_credential(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Login" in response.data
