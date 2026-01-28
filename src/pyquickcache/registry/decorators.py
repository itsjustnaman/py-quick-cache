from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..eviction_policy.base_eviction_policy import BaseEvictionPolicy
    from ..serializer.base_serializer import BaseSerializer


def register_eviction_policy(name: str):
    """
    Class decorator to register a custom eviction policy.

    Args:
        name (str): The name under which the eviction policy will be registered.

    Returns:
        Callable[[Type[BaseEvictionPolicy]], Type[BaseEvictionPolicy]]:
            A decorator that registers the given class as an eviction policy.

    Raises:
        TypeError: If the decorated class does not inherit from BaseEvictionPolicy.

    INTERNAL:
        Uses runtime import to avoid circular dependencies.
    """

    from ..eviction_policy.base_eviction_policy import BaseEvictionPolicy
    from .registry import _register_eviction_policy as _register

    def decorator(cls: Type["BaseEvictionPolicy"]) -> Type["BaseEvictionPolicy"]:
        if not issubclass(cls, BaseEvictionPolicy):
            raise TypeError(
                f"Eviction policy must inherit from BaseEvictionPolicy, got {cls.__name__}"
            )

        _register(name, cls)
        return cls

    return decorator


def register_serializer(name: str):
    """
    Class decorator to register a custom serializer.

    Args:
        name (str): The name under which the serializer will be registered.

    Returns:
        Callable[[Type[BaseSerializer]], Type[BaseSerializer]]:
            A decorator that registers the given class as a serializer.

    Raises:
        TypeError: If the decorated class does not inherit from BaseSerializer.

    INTERNAL:
        Uses runtime import to avoid circular dependencies.
    """

    from ..serializer.base_serializer import BaseSerializer
    from .registry import _register_serializer as _register

    def decorator(cls: Type["BaseSerializer"]) -> Type["BaseSerializer"]:
        if not issubclass(cls, BaseSerializer):
            raise TypeError(
                f"Serializer must inherit from BaseSerializer, got {cls.__name__}"
            )

        _register(name, cls)
        return cls

    return decorator
