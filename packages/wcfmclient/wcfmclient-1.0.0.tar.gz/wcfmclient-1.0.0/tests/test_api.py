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
    api, _ = setUp
    assert isinstance(api, API)


def test_get_url(setUp):
    api, _ = setUp
    assert api.get_url() == options.get("url")


def test_create_product(setUp):
    api, _ = setUp
    res = api.post("wp-json/wcfmmp/v1/products/", {
            "name": "Test Product",
            "slug": "test-product",
            "post_author": "11",
            "type": "simple",
            "status": "publish",
            "featured": False
        })

    assert res.status_code == 200
    assert isinstance(res.json(), dict)


def test_get_products(setUp):
    api, _ = setUp
    res = api.get("wp-json/wcfmmp/v1/products/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_orders(setUp):
    api, _ = setUp
    res = api.get("wp-json/wcfmmp/v1/orders/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_restricted_capabilities(setUp):
    api, _ = setUp
    res = api.get("wp-json/wcfmmp/v1/restricted-capabilities/")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)


def test_get_notifications(setUp):
    api, _ = setUp
    res = api.get("wp-json/wcfmmp/v1/notifications/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
