import asynctest as asynctest
from aioresponses import aioresponses

from .manager import Manager


class ManagerTestCase(asynctest.TestCase):
    async def setUp(self) -> None:
        self._manager = Manager.configure()

    async def tearDown(self) -> None:
        Manager.shared_instance = None

    def test_create_instance(self):
        # `self._manager`
        self.assertEqual(self._manager, Manager.get_instance())

    def test_prevents_reconfigure(self):
        def _attempt_reconf():
            Manager.configure()
        self.assertRaises(Exception, _attempt_reconf)

    def test_manager_has_module_managers(self):
        self.assertTrue(hasattr(self._manager, 'sessions'))
        self.assertTrue(hasattr(self._manager, 'engine'))


class ManagerMockedAPITestCase(asynctest.TestCase):
    async def setUp(self) -> None:
        self._manager = Manager.configure()

    async def tearDown(self) -> None:
        Manager.shared_instance = None

    async def test_health_check_fails_with_exception(self):
        with aioresponses() as mocked:
            mocked.get('http://localhost:10021/_health', status=500)

            async def _run():
                await self._manager.check_health(fail_silently=False)

            self.assertAsyncRaises(_run, Exception)

    async def test_health_check_fails_with_bool(self):
        with aioresponses() as mocked:
            mocked.get('http://localhost:10021/_health', status=500)

            status = await self._manager.check_health(fail_silently=True)

            self.assertEqual(status, False)

    async def test_health_check_passes(self):
        with aioresponses() as mocked:
            mocked.get('http://localhost:10021/_health', status=200)
            self.assertTrue(await self._manager.check_health(fail_silently=True))

            mocked.get('http://localhost:10021/_health', status=200)
            self.assertTrue(await self._manager.check_health(fail_silently=False))

    def test_sync_health_check(self):
        with aioresponses() as mocked:
            mocked.get('http://localhost:10021/_health', status=200)
            self.assertTrue(self._manager.check_health_sync(fail_silently=True))

