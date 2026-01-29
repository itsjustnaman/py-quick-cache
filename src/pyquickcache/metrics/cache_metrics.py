from .base import BaseMetrics
from dataclasses import dataclass, asdict


@dataclass
class CacheMetricsData:
    """
    Container for all cache metrics counters and derived statistics.

    This class stores raw counters (hits, misses, evictions, etc.)
    and exposes calculated properties such as hit ratio and eviction rate.

    It is intentionally kept as a pure data object with no side effects.
    """

    hits: int = 0
    """Number of successful cache hits."""

    misses: int = 0
    """Number of cache misses."""

    sets: int = 0
    """Number of successful set operations."""

    gets: int = 0
    """Total number of get operations attempted."""

    failed_ops: int = 0
    """Number of failed cache operations."""

    evictions: int = 0
    """Number of entries evicted due to eviction policy."""

    expired_removals: int = 0
    """Number of expired entries removed automatically."""

    manual_deletions: int = 0
    """Number of entries manually deleted by the user."""

    current_valid_keys: int = 0
    """Current number of non-expired keys in the cache."""

    peak_valid_keys: int = 0
    """Highest observed number of valid keys."""

    current_total_keys: int = 0
    """Current total number of keys (including expired)."""

    peak_total_keys: int = 0
    """Highest observed total number of keys."""

    # --- Calculated Properties ---

    @property
    def hit_ratio(self) -> float:
        """
        Ratio of get operations to set operations.

        Returns:
            float: Get-to-set ratio.
        """
        return (self.hits / self.gets) if self.gets > 0 else 0.0

    @property
    def miss_ratio(self) -> float:
        """
        Ratio of cache misses to total get operations.

        Returns:
            float: Miss ratio in the range [0.0, 1.0].
        """
        return (self.misses / self.gets) if self.gets > 0 else 0.0

    @property
    def get_set_ratio(self) -> float:
        """
        Ratio of get operations to set operations.

        Returns:
            float: Get-to-set ratio.
        """
        return (self.gets / self.sets) if self.sets > 0 else 0.0

    @property
    def eviction_rate(self) -> float:
        """
        Ratio of evictions to set operations.

        Returns:
            float: Eviction rate.
        """
        return (self.evictions / self.sets) if self.sets > 0 else 0.0

    @property
    def expired_bloat(self) -> int:
        """
        Number of expired entries currently occupying cache storage.

        Returns:
            int: Expired but not yet cleaned keys.
        """
        return self.current_total_keys - self.current_valid_keys

    @property
    def waste_percentage(self) -> float:
        """
        Percentage of cache occupied by expired entries.

        Returns:
            float: Waste percentage in the range [0.0, 100.0].
        """
        return (
            (self.expired_bloat / self.current_total_keys * 100)
            if self.current_total_keys > 0
            else 0.0
        )

    def to_dict(self):
        """
        Convert metrics data to a fully serializable dictionary.

        Includes both raw counters and derived metrics.

        Returns:
            dict: Dictionary representation of metrics.
        """
        data = asdict(self)

        data.update(
            {
                "hit_ratio": self.hit_ratio,
                "miss_ratio": self.miss_ratio,
                "get_set_ratio": self.get_set_ratio,
                "eviction_rate": self.eviction_rate,
                "expired_bloat": self.expired_bloat,
                "waste_percentage": self.waste_percentage,
            }
        )

        return data


class CacheMetrics(BaseMetrics):
    """
    Default in-memory metrics implementation for QuickCache.

    This class records cache metrics using simple integer counters
    and derives useful statistics such as hit ratio and eviction rate.

    Characteristics:
        - Lightweight and fast
        - Thread-safe by design assumption (GIL-protected increments)
        - Never raises exceptions
        - Safe to disable by replacing with NoOpMetrics
    """

    def __init__(self):
        self._data = CacheMetricsData()

    @property
    def hits(self) -> int:
        return self._data.hits

    @property
    def misses(self) -> int:
        return self._data.misses

    @property
    def gets(self) -> int:
        return self._data.gets

    @property
    def sets(self) -> int:
        return self._data.sets

    @property
    def failed_ops(self) -> int:
        return self._data.failed_ops

    @property
    def evictions(self) -> int:
        return self._data.evictions

    @property
    def expired_removals(self) -> int:
        return self._data.expired_removals

    @property
    def manual_deletions(self) -> int:
        return self._data.manual_deletions

    @property
    def current_valid_keys(self) -> int:
        return self._data.current_valid_keys

    @property
    def peak_valid_keys(self) -> int:
        return self._data.peak_valid_keys

    @property
    def current_total_keys(self) -> int:
        return self._data.current_total_keys

    @property
    def peak_total_keys(self) -> int:
        return self._data.peak_total_keys

    @property
    def hit_ratio(self) -> float:
        return self._data.hit_ratio

    @property
    def miss_ratio(self) -> float:
        return self._data.miss_ratio

    @property
    def get_set_ratio(self) -> float:
        return self._data.get_set_ratio

    @property
    def eviction_rate(self) -> float:
        return self._data.eviction_rate

    @property
    def expired_bloat(self) -> int:
        return self._data.expired_bloat

    @property
    def waste_percentage(self) -> float:
        return self._data.waste_percentage

    def record_set(self):
        self._data.sets += 1

    def record_hit(self):
        self._data.hits += 1

    def record_miss(self):
        self._data.misses += 1

    def record_failed_op(self):
        self._data.failed_ops += 1

    def record_get(self):
        self._data.gets += 1

    def record_eviction(self):
        self._data.evictions += 1

    def record_expired_removal(self):
        self._data.expired_removals += 1

    def record_manual_deletion(self):
        self._data.manual_deletions += 1

    def record_manual_deletions(self, count):
        self._data.manual_deletions += count

    def update_total_keys(self, length: int):
        self._data.current_total_keys = length
        if self._data.current_total_keys > self._data.peak_total_keys:
            self._data.peak_total_keys = self._data.current_total_keys

    def update_valid_keys(self, size: int):
        self._data.current_valid_keys = size
        if size > self._data.peak_valid_keys:
            self._data.peak_valid_keys = size

    def update_valid_keys_by_delta(self, delta: int):
        new_value = self._data.current_valid_keys + delta
        self._data.current_valid_keys = max(0, new_value)

        if self._data.current_valid_keys > self._data.peak_valid_keys:
            self._data.peak_valid_keys = self._data.current_valid_keys

    def snapshot(self):
        snapshot = self._data.to_dict()
        return snapshot

    def reset(self):
        self._data = CacheMetricsData()
