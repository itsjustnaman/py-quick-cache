from .base_eviction_policy import EvictionPolicy
from .lru import LRUEvictionPolicy
from .fifo import FIFOEvictionPolicy

# Optional: define __all__ to control what 'from eviction_policy import *' does
__all__ = ["EvictionPolicy", "LRUEvictionPolicy", "FIFOEvictionPolicy"]
