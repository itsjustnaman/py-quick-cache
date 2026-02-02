from collections import OrderedDict
from datetime import timedelta
from threading import RLock
from typing import Any, Optional
from enum import Enum, auto

from ..utils.helpers import utcnow
from .base import BaseCacheBackend
from ..exceptions import KeyExpired, KeyNotFound,  KeyAlreadyExists, InvalidTT

from ._cache_entry import CacheEntry


class KeyStatus(Enum):
    """
    INTERNAL.

    Represents the evaluated state of a cache key during lookup.

    Used by:
        - Internal inspection helpers
        - Public API methods to decide control flow without raising

    Values:
        MISSING:
            Key does not exist in the cache.

        EXPIRED:
            Key exists but has exceeded its TTL and was removed.

        VALID:
            Key exists and is not expired.
    """

    MISSING = auto()
    EXPIRED = auto()
    VALID = auto()


class InMemoryBackend(BaseCacheBackend):
    def __init__(self):

        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = RLock()

    def get(self, key: str) -> CacheEntry:
        with self._lock:
            key_status = self._inspect_key(key=key)
            if key_status is KeyStatus.MISSING:
                raise KeyNotFound
            
            if key_status is KeyStatus.EXPIRED:
                raise KeyExpired
            
            return self._store[key]
            
    def set(self, key: str, value: Any, ttl: int) -> None:
        with self._lock:
            entry = self._build_entry(value=value, ttl=ttl)
            self._write_entry(key=key, entry=entry)

    def add(self, key: str, value: Any, ttl: int) -> None:
        with self._lock:
            key_status = self._inspect_key(key=key)

            if key_status is KeyStatus.VALID:
                raise KeyAlreadyExists
            
            if key_status is KeyStatus.EXPIRED:
                self._store.pop(key)

            entry = self._build_entry(value=value, ttl=ttl)
            self._write_entry(key=key, entry=entry)

    def update(self, key: str, value: Any, ttl: int) -> None:
        with self._lock:
            key_status = self._inspect_key(key=key)

            if key_status is KeyStatus.MISSING:
                raise KeyNotFound
            
            if key_status is KeyStatus.EXPIRED:
                self._store.pop(key)
                raise KeyExpired
            
            new_entry = self._build_entry(value=value, ttl=ttl)
            self._write_entry(key=key, entry=new_entry)

    def delete(self, key: str) -> None:
        with self._lock:
            key_status = self._inspect_key(key=key)
            
            if key_status is KeyStatus.MISSING:
                raise KeyNotFound
            
            if key_status is KeyStatus.EXPIRED:
                raise KeyExpired
            
            self._store.pop(key)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def contains(self, key: str) -> bool:
        with self._lock:
            key_status = self._inspect_key(key=key)

            if (key_status is KeyStatus.MISSING) or (key_status is KeyStatus.EXPIRED):
                return False
            
            return True
    
    def _build_entry(self, value: Any, ttl: int) -> CacheEntry:
        entry = CacheEntry(
            value=value,
            expiration_time = utcnow() + timedelta(seconds=ttl),
            ttl=ttl
        ) 
        return entry
    
    def _write_entry(self, key: str, entry: CacheEntry):
        self._store[key] = entry

    def _inspect_key(self, key: str) -> KeyStatus:
        if key not in self._store:
            return KeyStatus.MISSING
        
        if self._store[key].is_expired():
            self._store.pop(key)
            return KeyStatus.EXPIRED
        
        return KeyStatus.VALID