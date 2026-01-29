from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseCacheBackend(ABC):
    """
    Backend interface for cache data
    """

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    @abstractmethod
    def add(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    @abstractmethod
    def update(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def contains(self, key: str):
        pass
