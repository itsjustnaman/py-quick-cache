from collections import OrderedDict
from .base import BaseEvictionPolicy

from ..registry.decorators import register_eviction_policy


@register_eviction_policy("fifo")
class FIFOEvictionPolicy(BaseEvictionPolicy):
    """
    First In First Out (FIFO) eviction policy.

    This policy evicts the oldest inserted item when the cache exceeds
    its capacity. It preserves insertion order using an OrderedDict.

    Registered as "fifo" in the eviction policy registry.

    INTERNAL:
        Subclasses BaseEvictionPolicy and implements required lifecycle methods.
    """

    def on_add(self, cache, key) -> None:
        """
        Handles a newly added key.

        Moves the key to the end to preserve insertion order.

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
        Called when an existing key is updated.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being updated.

        INTERNAL:
            No operation for FIFO; order does not change.
        """
        pass

    def on_access(self, cache: OrderedDict, key: str) -> None:
        """
        Called when a key is accessed.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being accessed.

        INTERNAL:
            No operation for FIFO; access does not affect eviction order.
        """
        pass

    def on_delete(self, cache, key) -> None:
        """
        Called when a key is explicitly deleted.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being deleted.

        INTERNAL:
            No operation needed for FIFO.
        """
        pass

    def select_eviction_key(self, cache: OrderedDict) -> str:
        """
        Selects the key to evict when the cache is full.

        Args:
            cache (OrderedDict): The cache's internal storage.

        Returns:
            str: The oldest key in the cache (first inserted).

        Raises:
            RuntimeError: If called when the cache is empty.

        INTERNAL:
            Overrides BaseEvictionPolicy.select_eviction_key.
        """
        if not cache:
            raise RuntimeError("Eviction requested on empty cache")
        return next(iter(cache))
