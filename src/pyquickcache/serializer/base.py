from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """
    Abstract base class for all serializers.

    This class defines the interface for serialization strategies. Every new
    serializer (e.g., JSON, Pickle, Protobuf) must implement these methods
    to convert Python objects to a storable format and back.

    Notes:
        - Subclasses must define the `extension` and `is_binary` properties.
        - Subclasses must implement `serialize` and `deserialize` methods.
        - Register custom serializers in `defaults.py` for default usage.

    INTERNAL:
        Do not instantiate directly; use a concrete subclass.
    """

    @property
    @abstractmethod
    def extension(self) -> str:
        """
        Returns the file extension associated with this serializer.

        Returns:
            str: File extension (e.g., 'json', 'pkl').

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @property
    @abstractmethod
    def is_binary(self) -> bool:
        """
        Indicates whether the serializer works with binary data.

        Returns:
            bool: True if the serializer requires binary I/O, False otherwise.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def serialize(self, data: Any) -> str | bytes:
        """
        Serializes a Python object into a string or bytes.

        Args:
            data (Any): The Python object to serialize.

        Returns:
            str | bytes: Serialized representation of the object.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def deserialize(self, data: str | bytes) -> Any:
        """
        Deserializes a string or bytes back into a Python object.

        Args:
            data (str | bytes): Serialized data to convert back to a Python object.

        Returns:
            Any: The deserialized Python object.

        INTERNAL:
            Must be implemented by subclasses.
        """
        pass
