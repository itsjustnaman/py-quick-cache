from collections import OrderedDict
from .base_eviction_policy import BaseEvictionPolicy

from ..registry.decorators import register_eviction_policy


@register_eviction_policy("lfu")
class LFUEvictionPolicy(BaseEvictionPolicy):
    """
    Least Frequently Used (LFU) eviction policy with LRU tie-breaking.

    This policy evicts the least frequently used item when the cache exceeds
    its capacity. Frequency is incremented on add, update, set, or access.
    In case of ties (multiple items with the same frequency), the least recently
    used item is evicted (LFU + LRU behavior).

    Registered as "lfu" in the eviction policy registry.

    INTERNAL:
        Subclasses BaseEvictionPolicy and manages internal frequency tables.
    """

    def __init__(self):
        """
        Initialize LFU eviction policy data structures.

        Attributes:
            freq (dict[str, int]): Maps keys to their access frequency.
            freq_table (dict[int, OrderedDict[str, None]]): Maps frequency to an
                OrderedDict of keys (preserving LRU order within the same frequency).
            min_freq (int): Tracks the current minimum frequency in the cache.

        INTERNAL:
            Used to maintain LFU state.
        """

        # keys -> frequency
        self.freq: dict[str, int] = {}

        # frequemcy -> ordered keys
        self.freq_table: dict[int, OrderedDict[str, None]] = {}

        # track current minimum frequency
        self.min_freq: int = 0

    def on_add(self, cache, key) -> None:
        """
        Called when a new key is inserted into the cache.

        Initializes frequency tracking for the new key and updates min_freq.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being added.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_add.
        """
        frequency = 1

        # Track frequency
        self.freq[key] = frequency

        # Ensure bucket exists
        if frequency not in self.freq_table:
            self.freq_table[frequency] = OrderedDict()

        # Insert at end (most recent within freq=1)
        self.freq_table[frequency][key] = None

        # New keys always reset min frequency
        self.min_freq = frequency

    def on_update(self, cache: OrderedDict, key: str) -> None:
        """
        Called when an existing key is updated.

        Increments the key's frequency and adjusts internal structures.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being updated.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_update.
        """
        self._touch(key=key)

    def on_access(self, cache: OrderedDict, key: str) -> None:
        """
        Called when a key is accessed.

        Increments the key's frequency and adjusts internal structures.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being accessed.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_access.
        """
        self._touch(key=key)

    def on_delete(self, cache, key) -> None:
        """
        Called when a key is explicitly removed from the cache.

        Removes the key from frequency tracking and updates min_freq if needed.

        Args:
            cache (OrderedDict): The cache's internal storage.
            key (str): The key being deleted.

        INTERNAL:
            Overrides BaseEvictionPolicy.on_delete.
        """
        freq = self.freq.pop(key)

        bucket = self.freq_table[freq]
        bucket.pop(key)

        # Clean up empty bucket
        if not bucket:
            del self.freq_table[freq]

            # Fix min_freq if needed
            if self.min_freq == freq:
                self.min_freq = min(self.freq_table.keys(), default=0)

    def select_eviction_key(self, cache: OrderedDict) -> str:
        """
        Selects the key to evict when the cache exceeds capacity.

        Args:
            cache (OrderedDict): The cache's internal storage.

        Returns:
            str: The least frequently used key; ties are broken by LRU order.

        Raises:
            RuntimeError: If called when the cache is empty.

        INTERNAL:
            Overrides BaseEvictionPolicy.select_eviction_key.
        """
        if not cache:
            raise RuntimeError("Eviction requested on empty cache")

        bucket = self.freq_table[self.min_freq]

        return next(iter(bucket))

    def _touch(self, key: str) -> None:
        """
        Internal helper to update the frequency of a key on access or update.

        Args:
            key (str): The key whose frequency is being updated.

        INTERNAL:
            Used internally by on_access and on_update to maintain LFU state.
        """
        old_freq = self.freq[key]
        new_freq = old_freq + 1
        self.freq[key] = new_freq

        bucket = self.freq_table[old_freq]
        bucket.pop(key)

        if not bucket:
            del self.freq_table[old_freq]
            if self.min_freq == old_freq:
                self.min_freq = min(self.freq_table.keys(), default=new_freq)

        if new_freq not in self.freq_table:
            self.freq_table[new_freq] = OrderedDict()

        self.freq_table[new_freq][key] = None
