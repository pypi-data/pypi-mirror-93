## WCFM ReST API Client

### Installation
This library is distributed on `pypi`. In order to add it as a dependency, run the following command:

``` sh
$ pip install wcfmclient
```
or

``` sh
$ pip3 install wcfmclient
```

### Prerequisite
This library is built in consideration with [JWT Authentication for WP REST API](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/).
Make sure that you follow WCFM's official authentication setup [here](https://docs.wclovers.com/wcfm-app/).

### Using the client library
Instantiate an API object as shown below
``` python
    from wcfmclient.api import API
    from wcfmclient.jwt_auth_service import JWTAuthService
    from wcfmclient.session import session

    api = API(**{
        "username": "vendor's username",
        "password": "vendor's password",
        "url": "https://your.domain.name",
        "session": session
    })
```

Authenticate with your store's server.

``` python
    from wcfmclient.api import API
    from wcfmclient.jwt_auth_service import JWTAuthService
    from wcfmclient.session import session

    api = API(**{
        "username": "vendor's username",
        "password": "vendor's password",
        "url": "https://your.domain.name",
        "session": session
    })

    jwt_auth_service = JWTAuthService(api)
    jwt_auth_service.authenticate()
```

Consuming wcfm rest api.

``` python
    from wcfmclient.api import API
    from wcfmclient.jwt_auth_service import JWTAuthService
    from wcfmclient.session import session

    api = API(**{
        "username": "vendor's username",
        "password": "vendor's password",
        "url": "https://your.domain.name",
        "session": session
    })

    jwt_auth_service = JWTAuthService(api)
    jwt_auth_service.authenticate()

    res = api.get("wp-json/wcfmmp/v1/products/")
    products = res.json()
```
