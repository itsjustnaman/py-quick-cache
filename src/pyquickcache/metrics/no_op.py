from .base_metrics import BaseMetrics


class NoOpMetrics(BaseMetrics):
    """
    No-operation metrics implementation.

    This class disables all metrics collection while preserving the
    `BaseMetrics` interface. All methods are safe, fast, and side-effect free.

    Intended use cases:
        - Disabling metrics for performance-critical workloads
        - Testing and benchmarking
        - Default fallback when metrics are not configured

    This implementation never raises exceptions and always returns
    empty or neutral values.
    """

    def record_set(self):
        """Ignore set operation metrics."""
        pass

    def record_get(self):
        """Ignore get operation metrics."""
        pass

    def record_hit(self):
        """Ignore cache hit metrics."""
        pass

    def record_miss(self):
        """Ignore cache miss metrics."""
        pass

    def record_failed_op(self):
        """Ignore failed operation metrics."""
        pass

    def record_eviction(self):
        """Ignore eviction metrics."""
        pass

    def record_expired_removal(self):
        """Ignore expired entry removal metrics."""
        pass

    def record_manual_deletion(self):
        """Ignore manual deletion metrics."""
        pass

    def update_total_keys(self, length: int):
        """Ignore total key count updates."""
        pass

    def update_valid_keys(self, size: int):
        """Ignore valid key count updates."""
        pass

    def update_valid_keys_by_delta(self, delta: int):
        """Ignore incremental valid key updates."""
        pass

    def snapshot(self) -> dict:
        """
        Return an empty metrics snapshot.

        Returns:
            dict: Always an empty dictionary.
        """
        return {}

    def reset(self):
        """Reset metrics state (no-op)."""
        pass
