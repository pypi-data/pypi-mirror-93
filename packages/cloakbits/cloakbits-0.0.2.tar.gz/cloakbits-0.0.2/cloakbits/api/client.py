import asyncio
import aiohttp

from cloakbits.exceptions import ManagerErrorResponse


class LocalAPIClient(object):
    def __init__(self, hostname: str, port: int):
        self._base_url = f"http://{hostname}:{port}/"
        self._client = aiohttp.ClientSession()

    async def post(self, url: str, payload: dict):
        _r = await self._client.post(self._base_url + url, json=payload)
        if _r.status >= 300:
            raise ManagerErrorResponse(_r.json())
        return await _r.json()

    async def get(self, url: str):
        _r = await self._client.get(self._base_url + url)
        return await _r.json()

    async def health(self):
        return await self._client.get(self._base_url + '_health')

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._client.close())
