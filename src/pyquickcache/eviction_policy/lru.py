from collections import OrderedDict
from .base import BaseEvictionPolicy

from ..registry.decorators import register_eviction_policy


@register_eviction_policy("lru")
class LRUEvictionPolicy(BaseEvictionPolicy):
    """
    Least Recently Used (LRU) eviction policy.

    This policy evicts the least recently accessed item when the cache exceeds
    its capacity. Access, addition, or update of a key moves it to the end of
    the OrderedDict to mark it as recently used.

    Registered as "lru" in the eviction policy registry.

    INTERNAL:
        Subclasses BaseEvictionPolicy and implements lifecycle methods.
    """

    def on_add(self, cache, key) -> None:
        """
        Handles a newly added key.

        Moves the key to the end to mark it as recently used.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key that was added.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_add.
        """
        if key in cache:
            cache.move_to_end(key)

    def on_update(self, cache: OrderedDict, key: str) -> None:
        """
        Handles an existing key being updated.

        Moves the key to the end to mark it as recently used.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being updated.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_update.
        """
        if key in cache:
            cache.move_to_end(key)

    def on_access(self, cache: OrderedDict, key: str) -> None:
        """
        Handles a key being accessed.

        Moves the key to the end to mark it as recently used.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being accessed.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_access.
        """
        if key in cache:
            cache.move_to_end(key)

    def on_delete(self, cache, key) -> None:
        """
        Called when a key is explicitly deleted.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being deleted.

        INTERNAL:
            No operation needed for LRU.
        """
        pass

    def select_eviction_key(self, cache: OrderedDict) -> str:
        """
        Selects the key to evict when the cache is full.

        In case of LRu, he first key in the OrderedDict is the least recently used.

        Args:
            cache (OrderedDict): The cache's internal storage.

        Returns:
            str: The least recently used key (first in the OrderedDict).

        Raises:
            RuntimeError: If called when the cache is empty.

        INTERNAL:
            Overrides BaseEvictionPolicy.select_eviction_key.
        """
        if not cache:
            raise RuntimeError("Eviction requested on empty cache")
        return next(iter(cache))
