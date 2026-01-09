"""Objectives: 
    [-] Store key-value pairs in a dictionary
    [-] Implement TTL (Time To Live) functionality for cache entries
    [-] Remove expired entries automatically
    [-] Provide methods to get, set, and delete cache entries
    [-] Implement a method to print the current state of the cache
    [-] Convert the code into a class-based structure for better organization
    [-] Implement a method to get the current size of the cache
    [-] Implement a method to cleanup the expired entries in the cache
    [-] Background cleanup to handle expired items automatically.
    [-] Implement LRU (Least Recently Used) eviction for cache size management.
    [-] Implement pluggable eviction policies (Strategy Pattern).
    [-] Ensure thread safety for concurrent access.
    [-] Enhance expiry strategies to allow more flexibility.
    [-] Make the cache entry and cache response more clear, e.g., using a dataclass or namedtuple.
    [] Make the cache persistent to survive application restarts.

"""

import time
from typing import Any, Optional
from datetime import datetime, timedelta 
from collections import OrderedDict
import threading
from dataclasses import dataclass

from eviction_policies import EvictionPolicy, LRUEvictionPolicy

@dataclass(slots=True)
class CacheEntry:
    value: Any
    expiration_time: datetime
    ttl: int

    def is_expired(self) -> bool:
        """Returns true if expired"""
        return datetime.now() > self.expiration_time
    
@dataclass(slots=True)
class CacheResponse:
    success: bool
    message: str
    data: Optional[Any] = None


class InMemoryCache:
    """
    In-Memory Cache.
    """

    # Class-level constants
    ERROR_TTL_INVALID = "TTL must be a positive natural number"
    ERROR_KEY_NOT_EXIST = "Key doesn't exist or is expired"
    ERROR_KEY_EXISTS = "A valid Key already exists"
    
    CLEANUP_INTERVAL_SEC = 2
    MAX_CACHE_SIZE = 3


    def __init__(self, eviction_policy: EvictionPolicy = None) -> None:
        # Default to LRU if no policy is provided
        if eviction_policy is None:
            eviction_policy = LRUEvictionPolicy()
        
        self.eviction_policy = eviction_policy
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock: threading.RLock = threading.RLock()

        # Start background cleanup thread (deamon=True to make sure it exits with main program)
        self.cleanup_thread = threading.Thread(target=self._background_cleanup, daemon=True)
        self.cleanup_thread.start()


    def _is_expired(self, key: str) -> bool:
        return key in self.cache and self.cache[key].is_expired()
    

    def cleanup(self) -> tuple[bool, int, str]:
        with self._lock:
            expired_keys = set()

            for key in self.cache:
                if self.cache[key].is_expired():
                    expired_keys.add(key)

            for key in expired_keys:
                self.cache.pop(key)

            return (True, len(expired_keys), "Cleanup completed")
    

    def _ensure_capacity(self) -> tuple[bool, str]:
        self.cleanup()

        while self.size() >= self.MAX_CACHE_SIZE:
            evicted_key = self.eviction_policy.select_eviction_key(self.cache)
            self.cache.pop(evicted_key)

        return(True, "Cache capacity enforced. Items evicted to make room.")


    def add(self, key: str, value: Any, ttl_sec: int) -> CacheResponse:
        with self._lock:
            try:
                ttl = int(ttl_sec)
            except ValueError:
                return CacheResponse(False, self.ERROR_TTL_INVALID)
            
            if ttl <= 0:
                return CacheResponse(False, self.ERROR_TTL_INVALID)
            
            if (key in self.cache):
                # Key expiry check
                if (not self.cache[key].is_expired()):
                    return CacheResponse(False, self.ERROR_KEY_EXISTS)

            
            if self.size() >= self.MAX_CACHE_SIZE:
                self._ensure_capacity()

            # Add a new cache entry as no valid key exists
            self.cache[key] = CacheEntry(
                value=value,
                expiration_time=datetime.now() + timedelta(seconds=ttl),
                ttl=ttl_sec
            )

            # --- PLUGGABLE HOOK FOR EVICTION POLICY ---
            self.eviction_policy.on_update(self.cache, key)

            return CacheResponse(True, "Key added")
    

    def update(self, key: str, value: Any, ttl_sec: int) -> CacheResponse:
        with self._lock:
            try:
                ttl = int(ttl_sec)
            except ValueError: 
                return CacheResponse(False, self.ERROR_TTL_INVALID)
            
            if ttl <= 0:
                return CacheResponse(False, self.ERROR_TTL_INVALID)

            if key not in self.cache:
                return CacheResponse(False, self.ERROR_KEY_NOT_EXIST)

            self.cache[key] = CacheEntry(
                value=value,
                expiration_time=datetime.now() + timedelta(seconds=ttl),
                ttl=ttl_sec
            )
            
            # --- PLUGGABLE HOOK FOR EVICTION POLICY ---
            self.eviction_policy.on_update(self.cache, key)

            return CacheResponse(True, "Key updated")


    def get(self, key: str) -> CacheResponse:
        with self._lock:
            if key not in self.cache:
                return CacheResponse(False, self.ERROR_KEY_NOT_EXIST)

            if (self.cache[key].is_expired()):
                self.cache.pop(key)
                return CacheResponse(False, self.ERROR_KEY_NOT_EXIST)
            
            # --- PLUGGABLE HOOK FOR EVICTION POLICY ---
            self.eviction_policy.on_access(self.cache, key)

            return CacheResponse(True, self.cache[key].value)


    def delete(self, key: str) -> CacheResponse:
        with self._lock:
            if key not in self.cache:
                return CacheResponse(False, self.ERROR_KEY_NOT_EXIST)
            
            if self.cache[key].is_expired():
                self.cache.pop(key)
                return CacheResponse(False, self.ERROR_KEY_NOT_EXIST)
            
            self.cache.pop(key)
            return CacheResponse(True, "Key deleted")

    
    def print(self):
        with self._lock:
            print(f"\n\tIn Memory Cache\n")
            for key in list(self.cache.keys()):
                if self.cache[key].is_expired():
                    self.cache.pop(key)
                    continue

                print(f"\t\t{key} : {self.cache[key].value} : {self.cache[key].ttl}\n")
            print(f"\tEND\n")


    def size(self)-> int:
        with self._lock:
            return len(self.cache)
        
    
    def _background_cleanup(self)-> None:
        """Background task that runs periodically to remove expired items."""
        while True:
            time.sleep(self.CLEANUP_INTERVAL_SEC)
            self.cleanup()
