import time

import pytest
import api as service


@pytest.fixture
def api():
    return service.api


@pytest.mark.pony()
def test_users(api):
    r = api.requests.post("/auth/register", json={'test': 'test'})
    assert r.status_code == 400, r.json()
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test21'})
    assert r.status_code == 422, r.json()


@pytest.mark.pony()
def test_login(api):
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    r = api.requests.post("/auth/login", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 200, r.json()
    json_data = r.json()
    assert json_data['status'] == 'success'
    assert json_data['auth_token']

    r = api.requests.post("/auth/login", json={'username': 'non_existing', 'password': 'test'})
    assert r.status_code == 404, r.json()


@pytest.mark.pony()
def test_logout(api):
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.requests.post("/auth/login", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    r = api.requests.post("/auth/logout", headers=dict(
        Authorization='Bearer ' + resp_login.json()['auth_token']
    ))
    assert r.status_code == 200, r.json()


@pytest.mark.pony()
def test_invalid_logout(api):
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.requests.post("/auth/login", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    time.sleep(6)
    r = api.requests.post("/auth/logout", headers=dict(
        Authorization='Bearer ' + resp_login.json()['auth_token']
    ))
    assert r.status_code == 401, r.json()


@pytest.mark.pony()
def test_valid_blacklisted_token_logout(api, ponydb):
    r = api.requests.post("/auth/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.requests.post("/auth/login", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    auth_token = resp_login.json()['auth_token']
    blacklist_token = ponydb.BlacklistToken(token=auth_token)
    blacklist_token.flush()

    r = api.requests.post("/auth/logout", headers=dict(
        Authorization='Bearer ' + auth_token
    ))
    assert r.status_code == 401, r.json()
    assert r.json()['message'] == 'Token blacklisted. Please log in again.'


@pytest.mark.pony
def test_user(ponydb):
    user = ponydb.User(name='test', password='testpass')
    auth_token = user.encode_auth_token()
    assert isinstance(auth_token, bytes)


@pytest.mark.pony
def test_decode_auth_token(ponydb):
    user = ponydb.User(
        name='test',
        email='test@test.com',
        password='test'
    )
    user.flush()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert user.decode_auth_token(auth_token.decode("utf-8")) == 1
