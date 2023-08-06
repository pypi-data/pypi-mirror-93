from cloakbits.api.client import LocalAPIClient


class BaseManager(object):
    def __init__(self, api_client: LocalAPIClient):
        self._api_client = api_client
