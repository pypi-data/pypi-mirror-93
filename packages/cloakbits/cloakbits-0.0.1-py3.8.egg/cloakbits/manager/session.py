from typing import Union, Optional, Literal

from pydantic.main import BaseModel

from ._base import BaseManager
from ..utils import provide_sync

SessionPlatform = Literal["Win32", "Linux i686", "MacIntel", "MacPPC"]


class SessionWHParam(BaseModel):
    width: int
    height: int


class SessionMediaDevices(BaseModel):
    video_input: int
    audio_input: int
    audio_output: int


class SessionGeolocation(BaseModel):
    lat: str
    lng: str


class SessionParams(BaseModel):
    platform: SessionPlatform
    memory: Optional[int]
    cores: Optional[int]
    window: Optional[SessionWHParam]
    screen: Optional[SessionWHParam]
    persisted: Optional[bool]
    bluetooth: Optional[bool]
    media_devices: Optional[SessionMediaDevices]


@provide_sync
class SessionManager(BaseManager):
    __sync__ = ['create']

    async def create(self, session_params: Union[SessionParams, dict]):
        if isinstance(session_params, dict):
            session_params = SessionParams(**session_params)
        return (await self._api_client.post("session/create", session_params.dict()))['id']
