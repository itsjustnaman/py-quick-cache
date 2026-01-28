class CacheError(Exception):
    """
    Base class for all cache-related errors.

    Attributes:
        code (str): Error code identifying the type of cache error.
        message (str): Human-readable error message.

    INTERNAL:
        Subclass this for all custom cache exceptions.
    """

    code = "CACHE_ERROR"

    def __init__(self, message: str | None = None):
        """
        Initialize CacheError.

        Args:
            message (str | None): Optional custom error message. Defaults to class name.
        """
        super().__init__(message or self.__class__.__name__)
        self.message = message or self.__class__.__name__


class KeyNotFound(CacheError):
    """
    Raised when a requested key is not found in the cache.

    Attributes:
        code (str): 'KEY_NOT_FOUND'
        key (str): The missing key.
    """

    code = "KEY_NOT_FOUND"

    def __init__(self, key: str):
        """
        Initialize KeyNotFound error.

        Args:
            key (str): The key that was not found.
        """
        super().__init__(f"Key '{key}' not found")
        self.key = key


class KeyExpired(CacheError):
    """
    Raised when a requested key has expired.

    Attributes:
        code (str): 'KEY_EXPIRED'
        key (str): The expired key.
    """

    code = "KEY_EXPIRED"

    def __init__(self, key: str):
        """
        Initialize KeyExpired error.

        Args:
            key (str): The key that has expired.
        """

        super().__init__(f"Key '{key}' has expired")
        self.key = key


class KeyAlreadyExists(CacheError):
    """
    Raised when trying to insert a key that already exists in the cache.

    Attributes:
        code (str): 'KEY_ALREADY_EXISTS'
        key (str): The key that already exists.
    """

    code = "KEY_ALREADY_EXISTS"

    def __init__(self, key: str):
        """
        Initialize KeyAlreadyExists error.

        Args:
            key (str): The key that already exists.
        """

        super().__init__(f"Key '{key}' already exists")
        self.key = key


class InvalidTTL(CacheError):
    """
    Raised when a TTL (time-to-live) value is invalid.

    Attributes:
        code (str): 'INVALID_TTL'
        ttl (int): The invalid TTL value.
    """

    code = "INVALID_TTL"

    def __init__(self, ttl: int):
        """
        Initialize InvalidTTL error.

        Args:
            ttl (int): The invalid TTL value.
        """
        super().__init__(f"Invalid TTL value: {ttl}")
        self.ttl = ttl


class CacheSaveError(CacheError):
    """
    Raised when the cache cannot be saved to disk.

    Attributes:
        code (str): 'CACHE_SAVE_ERROR'
        filepath (str): Path to the file where saving failed.
        original_exception (Exception | None): Original exception causing the failure.
    """

    code = "CACHE_SAVE_ERROR"

    def __init__(self, filepath: str, original_exception: Exception | None = None):
        """
        Initialize CacheSaveError.

        Args:
            filepath (str): File path where save failed.
            original_exception (Exception | None): Original exception, if any.
        """
        message = f"Failed to save cache to disk: {filepath}"
        if original_exception:
            message += f" | {original_exception}"
        super().__init__(message)
        self.filepath = filepath
        self.original_exception = original_exception


class CacheLoadError(CacheError):
    """
    Raised when the cache cannot be loaded from disk.

    Attributes:
        code (str): 'CACHE_LOAD_ERROR'
        filepath (str): Path to the file that failed to load.
        original_exception (Exception | None): Original exception causing the failure.
    """

    code = "CACHE_LOAD_ERROR"

    def __init__(self, filepath: str, original_exception: Exception | None = None):
        """
        Initialize CacheLoadError.

        Args:
            filepath (str): File path that failed to load.
            original_exception (Exception | None): Original exception, if any.
        """
        message = f"Failed to load cache from disk: {filepath}"
        if original_exception:
            message += f" | {original_exception}"
        super().__init__(message)
        self.filepath = filepath
        self.original_exception = original_exception


class CacheMetricsSaveError(CacheError):
    """
    Raised when cache metrics cannot be saved to disk.

    Attributes:
        code (str): 'CACHE_METRICS_SAVE_ERROR'
        filepath (str): Path to the file where saving metrics failed.
        __cause__ (Exception | None): Original cause of the failure.
    """

    code = "CACHE_METRICS_SAVE_ERROR"

    def __init__(self, filepath: str, cause: Exception | None = None):
        """
        Initialize CacheMetricsSaveError.

        Args:
            filepath (str): File path where metrics save failed.
            cause (Exception | None): Original cause exception, if any.
        """
        super().__init__(f"Failed to save cache metrics to disk: {filepath}")
        self.filepath = filepath
        self.__cause__ = cause
