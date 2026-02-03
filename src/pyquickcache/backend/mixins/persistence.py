from abc import ABC, abstractmethod


class PersistenceMixin(ABC):
    """
    Optional backend capability for durable persistence.

    This mixin defines a persistence contract for cache backends that support
    explicitly saving and restoring their internal state to and from durable
    storage.

    Backends that maintain their own durability or persistence mechanisms
    (e.g., Redis, Memcached, managed external stores) are NOT expected to
    implement this mixin.

    Notes:
        - This mixin is optional and capability-based.
        - The main cache controller must not assume its presence.
        - Storage location, format, and serialization strategy are backend-
          specific and configured externally (typically via backend config).
    """

    @abstractmethod
    def save(self) -> None:
        """
        Persist the backend's current state to durable storage.

        Implementations should write all data required to reconstruct the
        backend's logical cache state at a later time.

        This method must be safe to call multiple times and should not mutate
        the in-memory state beyond what is required for persistence.

        Raises:
            BackendSaveError:
                If the backend fails to persist its state due to I/O errors,
                serialization issues, or invalid configuration.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        """Restore the backend's state from durable storage.

        Implementations should replace the current in-memory state with the
        restored state from persistent storage.

        Expired entries MAY be discarded during the load process.

        Raises:
            BackendLoadError:
                If the backend fails to restore state due to missing files,
                corrupted data, incompatible formats, or invalid configuration.
        """
        raise NotImplementedError
