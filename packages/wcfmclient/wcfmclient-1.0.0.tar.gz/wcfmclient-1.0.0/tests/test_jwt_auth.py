import pytest
from wcfmclient.api import API
from wcfmclient.jwt_auth_service import JWTAuthService
from data import options


@pytest.fixture
def setUp():
    api = API(**options)
    jwt_auth_service = JWTAuthService(api)
    jwt_auth_service.authenticate()

    return api, jwt_auth_service


def test_initialization(setUp):
    api, jwt_auth_service = setUp
    assert isinstance(jwt_auth_service, JWTAuthService)


def test_get_url(setUp):
    api, jwt_auth_service = setUp
    assert jwt_auth_service.api.get_url() == options.get("url")


def test_get_token(setUp):
    api, jwt_auth_service = setUp
    res = jwt_auth_service.get_token()
    res = res.json()
    assert "token" in res


def test_validate_token(setUp):
    api, jwt_auth_service = setUp
    res = jwt_auth_service.get_token()
    res = jwt_auth_service.validate_token(res.json().get("token"))
    assert res.json().get("code") == "jwt_auth_valid_token"


def test_authenticated_request(setUp):
    api, jwt_auth_service = setUp
    res = api.get("wp-json/wcfmmp/v1/products/")

    assert res.status_code == 200
    assert type(res.json()) == list
