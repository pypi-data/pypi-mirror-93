import requests
from requests.adapters import HTTPAdapter
from requests.packages import urllib3

DEFAULT_TIMEOUT = 60  # seconds
TOTAL_RETRY = 3
ALLOWED_METHODS = ["HEAD", "GET", "POST", "PUT", "PATCH", "OPTIONS"]
STATUS_FORCELIST = [429, 500, 502, 503, 504]

RETRY_KWARGS = {
    "total": TOTAL_RETRY,
    "status_forcelist": STATUS_FORCELIST
}


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super(TimeoutHTTPAdapter, self).__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super(TimeoutHTTPAdapter, self).send(request, **kwargs)


try:
    retry_strategy = urllib3.Retry(
        allowed_methods=ALLOWED_METHODS,
        **RETRY_KWARGS
    )
except TypeError:
    # NOTE remove once urllib3 1.26 is the minimum version
    retry_strategy = urllib3.Retry(
        method_whitelist=ALLOWED_METHODS,
        **RETRY_KWARGS
    )

adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)
