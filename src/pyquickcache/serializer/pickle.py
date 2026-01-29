from typing import Any
import pickle

from .base import BaseSerializer

from ..registry.decorators import register_serializer


@register_serializer("pickle")
class PickleSerializer(BaseSerializer):
    """
    Pickle serializer implementation of BaseSerializer.

    This serializer converts Python objects to a binary format using the
    `pickle` module and deserializes them back to Python objects.

    Registered as "pickle" in the serializer registry.

    INTERNAL:
        Subclasses BaseSerializer and implements required methods.
    """

    @property
    def extension(self) -> str:
        """
        Returns the file extension for Pickle files.

        Returns:
            str: The string 'pkl'.

        INTERNAL:
            Overrides BaseSerializer.extension.
        """

        return "pkl"

    @property
    def is_binary(self) -> bool:
        """
        Indicates that Pickle uses binary I/O.

        Returns:
            bool: True, since Pickle serializes to bytes.

        INTERNAL:
            Overrides BaseSerializer.is_binary.
        """
        return True

    def serialize(self, data: Any) -> str | bytes:
        """
        Serializes a Python object to a binary format using Pickle.

        Args:
            data (Any): Python object to serialize.

        Returns:
            bytes: Pickle binary representation of the object.

        INTERNAL:
            Overrides BaseSerializer.serialize.
        """
        return pickle.dumps(data)

    def deserialize(self, data: str | bytes) -> Any:
        """
        Deserializes Pickle binary data back into a Python object.

        Args:
            data (bytes | str): Pickle binary data to deserialize.

        Returns:
            Any: Python object deserialized from Pickle data.

        INTERNAL:
            Overrides BaseSerializer.deserialize.
        """
        return pickle.loads(data)
