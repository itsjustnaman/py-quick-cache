from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


class BaseMetrics(ABC):
    """
    Abstract base class defining the interface for cache metrics collection.

    This class provides a contract for recording cache-related events such as
    hits, misses, evictions, and state changes, without coupling the core cache
    logic to any specific metrics backend.

    Design guarantees:
        - Metric methods MUST NOT raise exceptions
        - Metric recording must be lightweight and non-blocking
        - Failure to record metrics must never affect cache correctness

    Thread safety:
        Implementations must be thread-safe, as metrics may be recorded from
        multiple threads concurrently.

    Extensibility:
        Custom metrics backends (e.g., Prometheus, StatsD, OpenTelemetry)
        should subclass this class and implement all abstract methods.
    """

    # ---------- Event recording ----------

    @abstractmethod
    def record_set(self):
        """
        Record a successful cache set operation.

        This method is called when a key-value pair is successfully stored
        in the cache.
        """
        pass

    @abstractmethod
    def record_get(self):
        """
        Record an attempted cache get operation.

        This method is called for every `get` invocation, regardless of
        whether it results in a hit or a miss.
        """
        pass

    @abstractmethod
    def record_hit(self):
        """
        Record a cache hit.

        A hit occurs when a requested key exists and has not expired.
        """
        pass

    @abstractmethod
    def record_miss(self):
        """
        Record a cache miss.

        A miss occurs when a requested key does not exist or has expired.
        """
        pass

    @abstractmethod
    def record_failed_op(self):
        """
        Record a failed cache operation.

        This includes failures due to invalid input, internal errors,
        or rejected operations.
        """
        pass

    @abstractmethod
    def record_eviction(self):
        """
        Record an eviction event.

        Evictions occur when entries are removed automatically due to
        capacity limits or eviction policy decisions.
        """
        pass

    @abstractmethod
    def record_expired_removal(self):
        """
        Record the removal of an expired cache entry.

        This is typically triggered during cleanup or lazy expiration.
        """
        pass

    @abstractmethod
    def record_manual_deletion(self):
        """
        Record the manual deletion of a single cache entry.

        This corresponds to explicit user-initiated delete operations.
        """
        pass

    @abstractmethod
    def record_manual_deletions(self, count):
        """
        Record the manual deletion of multiple cache entries.

        Args:
            count (int): Number of keys removed in the operation.
        """
        pass

    # ---------- State updates ----------

    @abstractmethod
    def update_total_keys(self, length: int):
        """
        Update the total number of keys currently stored in the cache.

        Args:
            length (int): Current total number of cache entries.
        """
        pass

    @abstractmethod
    def update_valid_keys(self, size: int):
        """
        Update the count of valid (non-expired) keys in the cache.

        Args:
            size (int): Number of valid cache entries.
        """
        pass

    @abstractmethod
    def update_valid_keys_by_delta(self, delta: int):
        """
        Increment or decrement the count of valid cache entries.

        Args:
            delta (int): Change in valid key count (positive or negative).
        """
        pass

    # ---------- Export / lifecycle ----------

    @abstractmethod
    def snapshot(self) -> dict:
        """
        Return a snapshot of the current metrics state.

        Returns:
            dict: A dictionary containing metric names and their values.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset all collected metrics to their initial state.

        This is typically used for testing or metric lifecycle management.
        """
        pass
