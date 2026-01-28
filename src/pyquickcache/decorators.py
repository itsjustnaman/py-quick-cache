"""
Exposes the registry decorators for external use.

This module re-exports the cache registry decorators so that users can
easily register custom serializers and eviction policies without importing
from the internal `registry` package directly.

Available Decorators:
    - register_eviction_policy: Class decorator to register a custom eviction policy.
    - register_serializer: Class decorator to register a custom serializer.

INTERNAL:
    Simply exposes decorators from `.registry.decorators`; does not implement any logic.
"""

from .registry.decorators import (
    register_eviction_policy,
    register_serializer,
)

__all__ = [
    "register_eviction_policy",
    "register_serializer",
]
