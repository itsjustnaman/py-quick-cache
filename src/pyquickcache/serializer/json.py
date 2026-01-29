from typing import Any
import json

from .base import BaseSerializer

from ..registry.decorators import register_serializer


@register_serializer("json")
class JsonSerializer(BaseSerializer):
    """
    JSON serializer implementation of BaseSerializer.

    This serializer converts Python objects to JSON strings and back. It
    produces human-readable JSON with indentation and works with text data,
    not binary.

    Registered as "json" in the serializer registry.

    JSON serializer only supports serializable types. For arbitrary objects, use Pickle

    INTERNAL:
        Subclasses BaseSerializer and implements required methods.
    """

    @property
    def extension(self) -> str:
        """
        Returns the file extension for JSON files.

        Returns:
            str: The string 'json'.

        INTERNAL:
            Overrides BaseSerializer.extension.
        """
        return "json"

    @property
    def is_binary(self) -> bool:
        """
        Indicates that JSON uses text, not binary, I/O.

        Returns:
            bool: False, since JSON is a text format.

        INTERNAL:
            Overrides BaseSerializer.is_binary.
        """
        return False

    def serialize(self, data: Any) -> str | bytes:
        """
        Serializes a Python object to a formatted JSON string.

        Args:
            data (Any): Python object to serialize (e.g., dict, list, etc.).

        Returns:
            str: JSON string representation of the object.

        INTERNAL:
            Overrides BaseSerializer.serialize.
        """
        return json.dumps(data, indent=4)

    def deserialize(self, data: str | bytes) -> Any:
        """
        Deserializes a JSON string back into a Python object.

        Args:
            data (str | bytes): JSON string to deserialize.

        Returns:
            Any: Python object represented by the JSON string.

        INTERNAL:
            Overrides BaseSerializer.deserialize.
        """
        return json.loads(data)
