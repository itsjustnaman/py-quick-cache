from abc import ABC, abstractmethod
from collections import OrderedDict


class BaseEvictionPolicy(ABC):
    """
    Strategy interface for cache eviction policies.

    Implementations (FIFO, LRU, LFU, etc.) receive lifecycle callbacks
    from the cache and decide which key to evict when capacity is exceeded.

    Notes:
        - Policies must NOT modify the cache size directly.
        - Eviction occurs only via `select_eviction_key`.
        - Custom policies should be registered in `defaults.py`.

    INTERNAL:
        Do not instantiate directly; subclass this to create custom eviction policies.
    """

    @abstractmethod
    def on_add(self, cache: OrderedDict, key: str) -> None:
        """
        Called when a new key is inserted into the cache.

        Triggered only when the key did not previously exist
        (or was expired and removed).

        Args:
            cache (OrderedDict): The cache's internal storage mapping keys to values.
            key (str): The key that was added.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def on_update(self, cache: OrderedDict, key: str) -> None:
        """
        Called when an existing, valid key's value is updated.

        This is NOT called for new insertions.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key that was updated.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def on_access(self, cache: OrderedDict, key: str) -> None:
        """
        Called when a key is successfully accessed (read).

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key that was accessed.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def on_delete(self, cache: OrderedDict, key: str) -> None:
        """
        Called when a key is explicitly removed from the cache.

        This does NOT include automatic removals due to eviction
        or expiration unless explicitly invoked by the cache.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being removed.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def select_eviction_key(self, cache: OrderedDict) -> str:
        """
        Determines which key should be evicted when the cache exceeds capacity.

        Args:
            cache (OrderedDict): The cache's internal storage.

        Returns:
            str: The key selected for eviction.

        INTERNAL:
            Must be implemented by subclasses.
            Does NOT modify the cache directly.
        """
        pass
