"""
JWTAuthService Class
Wrapper class for
    https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/
"""

__title__ = "jwt_auth_service_class"
__version__ = "1.0.0"
__author__ = "palanskiheji"
__license__ = "MIT"

ERR_CODES = [
    "[jwt_auth] invalid_username",
    "[jwt_auth] incorrect_password",
    "[jwt_auth] empty_username",
    "[jwt_auth] empty_password",
    "jwt_auth_invalid_token",
    "jwt_auth_bad_auth_header",
    "jwt_auth_failed"
]


class JWTAuthServiceError(Exception):
    pass


class JWTAuthService():
    def __init__(self, api):
        self.api = api

    def get_token(self):
        return self.api.post(
            "wp-json/jwt-auth/v1/token",
            data={
                "username": self.api.username,
                "password": self.api.password
            })

    def validate_token(self, token):
        return self.api.post(
            "wp-json/jwt-auth/v1/token/validate",
            None,
            headers={"Authorization": "Bearer {}".format(token)}
        )

    def authenticate(self):
        res = self.get_token()
        if res.status_code == 200:
            self.api._token = res.json().get("token")
            return

        code = res.json().get("code")
        if code in ERR_CODES:
            raise JWTAuthServiceError(res.json().get("message"))

        raise JWTAuthServiceError(res.text)
