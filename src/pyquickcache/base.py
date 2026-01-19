from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """
    Abstract interface for all cache backends.
    """

    @abstractmethod
    def get(self, key: str):
        """Retrieve value for key."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Insert or update value."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete key."""
        pass

    @abstractmethod
    def size(self) -> int:
        """Return number of items."""
        pass

    @abstractmethod
    def clear(self):
        """Remove all entries."""
        pass

    @abstractmethod
    def cleanup(self):
        """Remove expired entries."""
        pass
