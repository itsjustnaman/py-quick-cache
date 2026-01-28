from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """
    Abstract base class defining the interface for all cache backends.

    This class provides the blueprint for cache implementations, enforcing
    consistent method signatures for key-value operations, TTL handling,
    and cache maintenance.

    INTERNAL:
        Do not instantiate directly; implement a concrete subclass.
    """

    @abstractmethod
    def get(self, key: str):
        """
        Retrieve the value associated with a given key from the cache.

        Args:
            key (str): The key to look up.

        Returns:
            Any: The value associated with the key, or None if not found.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Insert a new key-value pair into the cache or update an existing key.

        Args:
            key (str): The key to set.
            value (Any): The value to store.
            ttl (Optional[int], optional): Time-to-live in seconds. Defaults to None.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def delete(self, key: str):
        """
        Delete a key and its value from the cache.

        Args:
            key (str): The key to delete.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """
        Return the number of items currently stored in the cache.

        Returns:
            int: Number of cached items.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Remove all entries from the cache, resetting it completely.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Remove expired entries from the cache based on their TTL.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass
