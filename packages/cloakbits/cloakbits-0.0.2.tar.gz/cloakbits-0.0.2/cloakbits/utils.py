import asyncio
from functools import wraps


def provide_sync(cls):
    """ Provides `*_sync` methods for fields listed in `__sync__` of wrapped cls """
    synced_methods = getattr(cls, '__sync__')
    for method in synced_methods:
        async_method = getattr(cls, method)
        def sync_method(*args, **kwargs):
            return asyncio.get_event_loop().run_until_complete(async_method(*args, **kwargs))
        setattr(cls, f"{method}_sync", wraps(async_method)(sync_method))
    return cls
