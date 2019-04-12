import datetime
import time

import pytest
from pony.orm import commit
from starlette.testclient import TestClient

from api import app


@pytest.fixture
def api():
    return TestClient(app)


@pytest.mark.pony()
def test_users(api):
    r = api.post("/register", json={'test': 'test'})
    assert r.status_code == 400, r.json()
    r = api.post("/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    r = api.post("/register", json={'username': 'test', 'password': 'test21'})
    assert r.status_code == 422, r.json()


@pytest.mark.pony()
def test_login(api):
    r = api.post("/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    r = api.post("/token", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 200, r.json()
    json_data = r.json()
    assert json_data['status'] == 'success'
    assert json_data['token']

    r = api.post("/token", json={'username': 'non_existing', 'password': 'test'})
    assert r.status_code == 404, r.json()


@pytest.mark.pony()
def test_logout(api):
    r = api.post("/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.post("/token", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    r = api.post("/logout", headers=dict(
        Authorization='Bearer ' + resp_login.json()['token']
    ))
    assert r.status_code == 200, r.json()


@pytest.mark.pony()
def test_invalid_logout(ponydb, api, monkeypatch):
    monkeypatch.setattr(ponydb.User, 'VALID_TOKEN_TIME', 1)
    r = api.post("/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.post("/token", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    time.sleep(2)
    r = api.post("/logout", headers=dict(
        Authorization='Bearer ' + resp_login.json()['token']
    ))
    assert r.status_code == 401, r.json()


@pytest.mark.pony()
def test_valid_blacklisted_token_logout(api, ponydb):
    r = api.post("/register", json={'username': 'test', 'password': 'test'})
    assert r.status_code == 201, r.json()
    resp_login = api.post("/token", json={'username': 'test', 'password': 'test'})
    assert resp_login.status_code == 200, resp_login.json()
    token = resp_login.json()['token']
    blacklist_token = ponydb.BlacklistToken(token=token)
    blacklist_token.flush()

    r = api.post("/logout", headers=dict(
        Authorization='Bearer ' + token
    ))
    assert r.status_code == 401, r.json()
    assert r.json()['message'] == 'Token blacklisted. Please log in again.'


@pytest.mark.pony
def test_user(ponydb):
    user = ponydb.User(name='test', password='testpass')
    token = user.encode_auth_token()
    assert isinstance(token, bytes)


@pytest.mark.pony
def test_decode_token(ponydb):
    user = ponydb.User(
        name='test',
        email='test@test.com',
        password='test'
    )
    user.flush()
    token = user.encode_auth_token(user.id)
    assert isinstance(token, bytes)
    assert user.decode_auth_token(token.decode("utf-8")) == 1


@pytest.mark.pony
def test_debtitem_list(api, ponydb, monkeypatch):

    def patched_auto_created(self):
        self.created = datetime.datetime(2019, 2, 7, 18, 22)

    def tomorrow_date():
        return (datetime.datetime.now() + datetime.timedelta(days=1)).date()

    user = ponydb.User(
        name='test',
        email='test@test.com',
        password='test'
    )

    monkeypatch.setattr(ponydb.DebtItem, 'before_insert', patched_auto_created)

    ponydb.DebtItem(
        kind='debt',
        due_date=tomorrow_date(),
        who="Marcin",
        what="Kniga",
        user=user
    )
    commit()

    token = user.encode_auth_token().decode()
    r = api.get("/api/items", headers={'Authorization': f'Bearer {token}'})

    expected = [{
        "name": 'test',
        "kind": 'debt',
        "created": "2019-02-07T18:22:00+00:00",
        "due_date": "2019-04-04",
        "who": "Marcin",
        "what": "Kniga",
        "resolved": "false"
    }]

    assert r.status_code == 200

    assert r.json() == expected
