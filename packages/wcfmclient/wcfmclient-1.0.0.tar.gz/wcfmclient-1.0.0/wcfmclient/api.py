
"""
WCFM API Class
"""

__title__ = "wcfm_api_class"
__version__ = "1.0.0"
__author__ = "palanskiheji"
__license__ = "MIT"


from json import dumps as jsonencode
from requests import Request


class API(object):
    fields = ["url", "username", "password", "session"]

    def __init__(self, **kwargs):
        self.__map_fields(kwargs)
        self._token = None

    def __map_fields(self, options):
        self.__validate_required(options)
        for key, value in options.items():
            if key in self.fields:
                setattr(self, key, value)

    def __validate_required(self, options):
        for field in self.fields:
            if field not in options:
                raise Exception("Required field {} is missing.".format(field))

    def __get_url(self, endpoint=""):
        url = self.url

        if not url.endswith("/"):
            url = "{}/".format(url)

        url = "{}{}".format(url, endpoint)
        return url

    def __get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "keep-alive"
        }
        if self._token:
            headers["Authorization"] = "Bearer {}".format(self._token)

        return headers

    def __request(self, method, endpoint, data, params={}, **kwargs):
        url = self.__get_url(endpoint)

        if data is not None:
            data = jsonencode(data)

        headers = self.__get_headers()

        if "headers" in kwargs:
            headers.update(kwargs.get("headers", {}))
            del kwargs["headers"]

        return self.session.send(
            self.session.prepare_request(
                Request(
                    method=method,
                    url=url,
                    auth=None,
                    params=params,
                    data=data,
                    headers=headers,
                    **kwargs
                )
            )
        )

    def get_url(self): return self.url

    def get(self, endpoint, **kwargs):
        return self.__request("GET", endpoint, None, **kwargs)

    def post(self, endpoint, data, **kwargs):
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.__request("DELETE", endpoint, None, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.__request("OPTIONS", endpoint, None, **kwargs)
