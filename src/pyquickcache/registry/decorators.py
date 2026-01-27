from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..eviction_policy.base_eviction_policy import BaseEvictionPolicy
    from ..serializer.base_serializer import BaseSerializer


def register_eviction_policy(name: str):
    """
    Class decorator to register a custom eviction policy.
    """

    # Runtime imports — safe, no circular import
    from ..eviction_policy.base_eviction_policy import BaseEvictionPolicy
    from .registry import register_eviction_policy as _register

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
    """

    from ..serializer.base_serializer import BaseSerializer
    from .registry import register_serializer as _register

    def decorator(cls: Type["BaseSerializer"]) -> Type["BaseSerializer"]:
        if not issubclass(cls, BaseSerializer):
            raise TypeError(
                f"Serializer must inherit from BaseSerializer, got {cls.__name__}"
            )

        _register(name, cls)
        return cls

    return decorator
