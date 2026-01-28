from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Returns the current UTC datetime with timezone info.

    Returns:
        datetime: Current date and time in UTC with timezone info.

    INTERNAL:
        Used internally for timestamping cache entries and metrics.
    """

    return datetime.now(timezone.utc)
