from __future__ import annotations

from typing import Type, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..eviction_policy import BaseEvictionPolicy
    from ..serializer import BaseSerializer

_EVICTION_POLICY_REGISTRY: Dict[str, Type[BaseEvictionPolicy]] = {}
_SERIALIZER_REGISTRY: Dict[str, Type[BaseSerializer]] = {}


def register_eviction_policy(name: str, cls: Type[BaseEvictionPolicy]) -> None:
    key = name.lower()
    if key in _EVICTION_POLICY_REGISTRY:
        raise ValueError(f"Eviction policy '{name}' already registered.")
    _EVICTION_POLICY_REGISTRY[key] = cls


def register_serializer(name: str, cls: Type[BaseSerializer]) -> None:
    key = name.lower()
    if key in _SERIALIZER_REGISTRY:
        raise ValueError(f"Serializer '{name}' already registered.")
    _SERIALIZER_REGISTRY[key] = cls


def create_eviction_policy(name: str) -> BaseEvictionPolicy:
    try:
        return _EVICTION_POLICY_REGISTRY[
            name.lower()
        ]()  # end parenthesis to return a class object
    except:
        raise ValueError(
            f"Unknown eviction policy '{name}'. "
            f"Available: {list(_EVICTION_POLICY_REGISTRY.keys())}"
        )


def create_serializer(name: str) -> BaseSerializer:
    try:
        return _SERIALIZER_REGISTRY[name.lower()]()
    except KeyError:
        raise ValueError(
            f"Unknown serializer '{name}'. "
            f"Available: {list(_SERIALIZER_REGISTRY.keys())}"
        )
