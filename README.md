# PyQuickCache

PyQuickCache is a high-performance, thread-safe in-memory caching library for Python with TTL support, pluggable eviction policies, metrics, and optional persistence.

## Features

- TTL-based expiration
- Pluggable eviction policies (LRU, FIFO, etc.)
- Thread-safe operations
- Background cleanup worker
- Metrics collection (hits, misses, evictions, etc.)
- Optional persistence (serializer + storage backend)
- Extensible architecture (custom eviction policies & serializers)

## Installation

```bash
pip install pyquickcache
```

## Quick Start

```python
from pyquickcache import QuickCache, QuickCacheConfig

cache = Cache(CacheConfig(max_size=100))

cache.set("user:1", {"name": "Alice"}, ttl=60)

result = cache.get("user:1")
print(result.data)
```

## Configuration

```python
config = CacheConfig(
    max_size=1000,
    default_ttl=60,
    cleanup_interval=5,
    enable_metrics=True
)
```

## Metrics

```python
snapshot = cache.get_metrics_snapshot()
print(snapshot)
```

## Eviction Policies

Built-in:
- LRU (default)

You can register your own:

```python
from pyquickcache import register_eviction_policy

register_eviction_policy("my_policy", MyPolicy)
```

## Persistence

```python
cache.save_to_disk()
cache.load_from_disk()
```

## Thread Safety

All operations are protected by re-entrant locks and safe for concurrent access.

## License

MIT License
