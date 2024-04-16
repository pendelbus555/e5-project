from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WComponent, Work, WorkComponent, Employee
import redis


def clear_cache_by_prefix(prefix):
    redis_connection = redis.Redis(host='redis', port=6379, db=0)
    keys = redis_connection.scan_iter(f'*{prefix}*')
    for key in keys:
        redis_connection.delete(key)


@receiver([post_save, post_delete], sender=Work)
@receiver([post_save, post_delete], sender=WComponent)
@receiver([post_save, post_delete], sender=WorkComponent)
def clear_works_cache(sender, instance, **kwargs):
    clear_cache_by_prefix('works')


@receiver([post_save, post_delete], sender=Employee)
def clear_works_cache(sender, instance, **kwargs):
    clear_cache_by_prefix('employees')
