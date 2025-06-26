import asyncio
import logging
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.db.models import QuerySet

logger = logging.getLogger("query_helper")
CACHE_LOCK_PREFIX = "lock_"
LOCK_TIMEOUT = 10

"""
get_sort_value(obj, key, sort_order)
------------------------------------
Helper function to get the sortable value for an object's attribute.
Handles special cases for date fields and missing values.

Args:
    obj: The object to extract the value from.
    key: The attribute name to sort by.
    sort_order: 'asc' or 'desc', used for handling None values in date fields.

Returns:
    The value to use for sorting, or a tuple for special cases.
"""


def get_sort_value(obj, key, sort_order):
    # Get the attribute value from the object, default to None if not present
    value = getattr(obj, key, None)
    # Special handling for date fields: if value is None, return a value that sorts last or first
    if key in ["publish_date", "update_date"] and value is None:
        # For ascending, None sorts before real dates; for descending, use 'ZZZ' to sort last
        return (None,) if sort_order == "asc" else ("ZZZ",)
    # For other fields, return empty string if value is None
    return value if value is not None else ""


"""
get_cached_filterd_data_async(
    text_filter: str,
    query_set: QuerySet,
    cache_key: str,
    filter_predicate,
    sort_by,
    sort_order,
)
----------------------------------------------------------
Async helper to retrieve, cache, filter, and sort queryset data.

- Checks if data is in cache. If not, acquires a lock and fetches from DB, then caches it for future use.
- Applies a filter predicate to the cached/queryset data if a text filter is provided.
- Sorts the filtered data by the specified field and order.

Args:
    text_filter: The text to filter objects by (case-insensitive).
    query_set: The Django QuerySet to fetch data from if not cached.
    cache_key: The cache key to use for storing/retrieving data.
    filter_predicate: Function to filter each object (should accept text_filter and object).
    sort_by: Field name to sort by.
    sort_order: 'asc' or 'desc'.

Returns:
    A sorted list of filtered objects.
"""


async def get_cached_filterd_data_async(
    text_filter: str,
    query_set: QuerySet,
    cache_key: str,
    filter_predicate,  # function for filter
    sort_by,
    sort_order,
):
    # Try to get data from cache
    values_data = cache.get(cache_key)
    if not values_data:
        # If not cached, acquire a lock to prevent race conditions
        lock_key = CACHE_LOCK_PREFIX + cache_key
        lock_acquired = await sync_to_async(cache.add)(lock_key, "locked", LOCK_TIMEOUT)
        if lock_acquired:
            try:
                # Double-check cache after acquiring lock (another request may have set it)
                values_data = cache.get(cache_key)
                if not values_data:
                    # If still not cached, fetch from DB and convert queryset to list
                    values_data = await sync_to_async(list)(query_set)
                    # Save the data in cache (default timeout)
                    cache.set(cache_key, values_data, timeout=86400)
            finally:
                # Release the lock so other requests can proceed
                await sync_to_async(cache.delete)(lock_key)
    # If a text filter is provided, filter the data using the predicate
    if text_filter:
        values_data = [
            value for value in values_data if filter_predicate(text_filter, value)
        ]

    # Sort the filtered data by the specified field and order
    result = sorted(
        values_data,
        key=lambda value: get_sort_value(value, sort_by, sort_order),
        reverse=(sort_order == "desc"),
    )

    return result
