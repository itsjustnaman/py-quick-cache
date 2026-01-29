from collections import OrderedDict
from datetime import datetime, timedelta
from threading import RLock
from typing import Any, Optional

from ..helpers import utcnow
from .base import BaseCacheBackend
from ..exceptions import KeyExpired, KeyNotFound

class InMemoryBackend(BaseCacheBackend):
    def __init__(self):
        self._store = OrderedDict()
        self._lock = RLock()

    def get(self, key: str):
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    def add(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    def update(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    def delete(self, key: str):
        pass

    def clear(self):
        pass

    def contains(self, key: str):
        pass