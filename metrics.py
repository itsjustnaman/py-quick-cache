from dataclasses import dataclass, asdict


@dataclass
class CacheMetricsData:
    hits: int = 0
    misses: int = 0
    sets: int = 0
    gets: int = 0
    failed_ops: int = 0
    evictions: int = 0
    expired_removals: int = 0
    manual_deletions: int = 0
    current_valid_keys: int = 0
    peak_valid_keys: int = 0
    current_total_keys: int = 0
    peak_total_keys: int = 0

    def to_dict(self):
        return asdict(self)


class CacheMetrics:
    def __init__(self):
        self._data = CacheMetricsData()

    def get_current_valid_keys(self) -> int:
        return self._data.current_valid_keys

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

    def update_total_keys(self, length: int):
        self._data.current_total_keys = length
        if self._data.current_total_keys > self._data.peak_total_keys:
            self._data.peak_total_keys = self._data.current_total_keys

    # RENAME TO update_valid_size
    def update_valid_keys(self, size: int):
        self._data.current_valid_keys = size
        if size > self._data.peak_valid_keys:
            self._data.peak_valid_keys = size

    def snapshot(self):
        snapshot = self._data.to_dict()

        snapshot["hit_ratio"] = (
            (self._data.hits / self._data.gets) if self._data.gets > 0 else 0.0
        )
        snapshot["miss_ratio"] = (
            (self._data.misses / self._data.gets) if self._data.gets > 0 else 0.0
        )
        snapshot["get_set_ratio"] = (
            (self._data.gets / self._data.sets) if self._data.sets > 0 else 0.0
        )
        snapshot["eviction_rate"] = (
            (self._data.evictions / self._data.sets) if self._data.sets > 0 else 0.0
        )
        snapshot["expired_removal_rate"] = (
            (self._data.expired_removals / self._data.gets)
            if self._data.gets > 0
            else 0.0
        )
        snapshot["expired_bloat"] = (
            self._data.current_total_keys - self._data.current_valid_keys
        )
        snapshot["waste_percentage"] = (
            (snapshot["expired_bloat"] / self._data.current_total_keys * 100)
            if self._data.current_total_keys > 0
            else 0.0
        )

        return snapshot
