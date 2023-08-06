from dataclasses import dataclass

from aiohttp import ClientConnectorError

from .session import SessionManager
from ..api.client import LocalAPIClient
from ..exceptions import ManagerConfigureException
from ..utils import provide_sync


@dataclass
class ManagerConfig:
    hostname: str
    port: int


default_config = ManagerConfig(hostname='localhost', port=10021)


@provide_sync
class Manager(object):
    __sync__ = ['check_health']
    shared_instance: 'Manager' = None

    def __init__(self, config: ManagerConfig):
        self._config = config
        self._api_client = LocalAPIClient(hostname=config.hostname, port=config.port)
        self._sessions = SessionManager(self._api_client)
        self._engine = None

    @staticmethod
    def configure(config: ManagerConfig = default_config):
        if Manager.shared_instance:
            raise ManagerConfigureException(".configure cannot be called twice!")
        Manager.shared_instance = Manager(config)
        return Manager.shared_instance

    @staticmethod
    def get_instance():
        return Manager.shared_instance

    @property
    def sessions(self):
        return self._sessions

    @property
    def engine(self):
        return self._engine

    async def check_health(self, fail_silently: bool = True):
        try:
            status = (await self._api_client.health()).status
        except ClientConnectorError:
            status = -1
        if status < 0 or status >= 300:
            if fail_silently:
                return False
            else:
                raise Exception()
        else:
            return True
