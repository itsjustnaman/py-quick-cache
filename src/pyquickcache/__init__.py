"""
pyquickcache

A fast, extensible in-memory caching library with TTL support,
pluggable eviction policies, persistence, and metrics.

This package exposes the public caching API.
"""

# Trigger registration of built-in serializers & eviction policies
from ._bootstrap import * 

from .cache import QuickCache
from .config import QuickCacheConfig
from .decorators import register_eviction_policy, register_serializer

# Load defaults on package import
# from .registry import default_registries

__all__ = [
    "Cache",
    "QuickCacheConfig",
    "register_eviction_policy",
    "register_serializer",
]
