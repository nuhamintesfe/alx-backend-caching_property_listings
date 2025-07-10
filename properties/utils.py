from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Returns all Property objects, using Redis cache for 1 hour.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, timeout=3600)
    return properties


def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and logs them.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        ratio = hits / total_requests if total_requests > 0 else 0

        logger.info(f"Redis Cache - Hits: {hits}, Misses: {misses}, Hit Ratio: {ratio:.2f}")
        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": ratio
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {str(e)}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0
        }