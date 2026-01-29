from abc import ABC, abstractmethod
from typing import Any


class StorageBackend(ABC):
    """
    INTERNAL.

    Abstract interface for cache persistence backends.
    """

    @abstractmethod
    def save(self, data: Any) -> None:
        pass

    @abstractmethod
    def load(self) -> Any:
        pass
