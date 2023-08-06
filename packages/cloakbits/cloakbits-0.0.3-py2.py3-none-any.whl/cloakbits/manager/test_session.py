from aioresponses import aioresponses
from asynctest import TestCase

from . import Manager
from .session import SessionParams


class SessionTestCase(TestCase):
    async def setUp(self) -> None:
        self._manager = Manager.configure()

    async def test_create_session(self):
        with aioresponses() as mocked:
            mocked.post('http://localhost:10021/session/create', status=200, payload={'id': 'test-id'})
            s_params: SessionParams = SessionParams(platform='Win32')
            ret_id = await self._manager.sessions.create(s_params)
            self.assertEqual(ret_id, 'test-id')



