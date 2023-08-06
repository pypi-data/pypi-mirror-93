import time
from unittest import mock

from fastapi import Header
from fastapi.testclient import TestClient
from pytest_mock import mocker

from insnail_ai_tools.sso import Sso
from insnail_ai_tools.web import create_fast_api_app

sso = Sso(
    "sso",
    "redis://@localhost:6379/1",
)

app = create_fast_api_app()
client = TestClient(app)


@app.get("/fun1")
@sso.fast_api_sso
def func1(token: str = Header(...)):
    return {"msg": "success"}


@app.get("/fun2")
def fun2(token: str = Header(...)):
    return {"msg": "success"}


def test_fast_api_sso():
    token = sso.generate_token("liqiongyu")

    sso._redis.sismember = mock.Mock(return_value=True)
    response = client.get("/fun1", headers={"token": token})
    assert response.json() == {"msg": "success"}
    sso._redis.sismember = mock.Mock(return_value=False)
    response = client.get("/fun1", headers={"token": "def"})
    assert response.status_code == 401
