from abc import ABC, abstractmethod
from typing import Any, Optional, Iterable, Dict


class BaseCacheBackend(ABC):
    """Abstract base class for cache storage backends.

    A cache backend is responsible **only** for storing and retrieving data.
    It does not implement eviction policies, metrics, logging, or public API
    semantics.

    This interface is designed to support multiple backend implementations
    such as:
        - In-memory
        - Filesystem
        - Redis / Memcached
        - Remote cache services

    All backend implementations must be synchronous and thread-safe unless
    explicitly documented otherwise.
    """

    # ─────────────────────────
    # Core key-value operations
    # ─────────────────────────

    @abstractmethod
    def get(self, key: str) -> Any:
        """Retrieve the value associated with a key.

        Args:
            key (str): The cache key to retrieve.

        Returns:
            Any: The stored value for the key.

        Raises:
            KeyNotFound: If the key does not exist.
            KeyExpired: If the key exists but has expired.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value for a key, overwriting any existing value.

        Args:
            key (str): The cache key to set.
            value (Any): The value to store.
            ttl (Optional[int]): Time-to-live in seconds. If None, the key
                does not expire.

        Returns:
            None
        """
        pass

    @abstractmethod
    def add(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Add a value for a key only if the key does not already exist.

        Args:
            key (str): The cache key to add.
            value (Any): The value to store.
            ttl (Optional[int]): Time-to-live in seconds.

        Raises:
            KeyAlreadyExists: If the key already exists.

        Returns:
            None
        """
        pass

    @abstractmethod
    def update(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Update the value of an existing key.

        Args:
            key (str): The cache key to update.
            value (Any): The new value.
            ttl (Optional[int]): Optional new TTL in seconds.

        Raises:
            KeyNotFound: If the key does not exist.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a key from the backend.

        Args:
            key (str): The cache key to delete.

        Raises:
            KeyNotFound: If the key does not exist.

        Returns:
            None
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all keys and values from the backend.

        Returns:
            None
        """
        pass

    @abstractmethod
    def contains(self, key: str) -> bool:
        """Check whether a key exists in the backend.

        Args:
            key (str): The cache key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        pass

    # ─────────────────────────
    # Bulk operations
    # ─────────────────────────

    @abstractmethod
    def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        """Retrieve multiple keys at once.

        Args:
            keys (Iterable[str]): An iterable of cache keys.

        Returns:
            Dict[str, Any]: A mapping of keys to values for keys that exist.
                Missing or expired keys are omitted.
        """
        pass

    @abstractmethod
    def set_many(
        self,
        mapping: Dict[str, Any],
        ttl: Optional[int] = None,
    ) -> None:
        """Set multiple key-value pairs at once.

        Args:
            mapping (Dict[str, Any]): A mapping of keys to values.
            ttl (Optional[int]): Optional TTL applied to all keys.

        Returns:
            None
        """
        pass

    @abstractmethod
    def delete_many(self, keys: Iterable[str]) -> None:
        """Delete multiple keys at once.

        Args:
            keys (Iterable[str]): An iterable of cache keys.

        Returns:
            None
        """
        pass

    # ─────────────────────────
    # Introspection
    # ─────────────────────────

    @abstractmethod
    def size(self) -> int:
        """Return the number of keys stored in the backend.

        Returns:
            int: Number of stored keys.
        """
        pass

    @abstractmethod
    def keys(self) -> Iterable[str]:
        """Return an iterable of all keys stored in the backend.

        Returns:
            Iterable[str]: All cache keys.
        """
        pass

    # ─────────────────────────
    # TTL / expiration handling
    # ─────────────────────────

    @abstractmethod
    def ttl(self, key: str) -> Optional[int]:
        """Return the remaining TTL for a key.

        Args:
            key (str): The cache key.

        Returns:
            Optional[int]: Remaining TTL in seconds, or None if the key
                does not expire.

        Raises:
            KeyNotFound: If the key does not exist.
        """
        pass

    @abstractmethod
    def expire(self, key: str, ttl: int) -> None:
        """Set or update the TTL for an existing key.

        Args:
            key (str): The cache key.
            ttl (int): New TTL in seconds.

        Raises:
            KeyNotFound: If the key does not exist.

        Returns:
            None
        """
        pass

    # ─────────────────────────
    # Lifecycle management
    # ─────────────────────────

    @abstractmethod
    def close(self) -> None:
        """Release backend resources and perform cleanup.

        This method is called when the cache is shutting down and may be used
        to:
            - Close file handles
            - Flush buffers
            - Close network connections

        Returns:
            None
        """
        pass
