from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WComponent, Work, WorkComponent, Employee, Vacancy,VComponent,VacancyComponent,Company, News, Rubric, Partner
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



@receiver([post_save, post_delete], sender=Vacancy)
@receiver([post_save, post_delete], sender=VComponent)
@receiver([post_save, post_delete], sender=VacancyComponent)
@receiver([post_save, post_delete], sender=Company)
def clear_vacancy_page(sender, instance, **kwargs):
    clear_cache_by_prefix('index')
    clear_cache_by_prefix('vacancy')
    clear_cache_by_prefix('vacancy_single')

@receiver([post_save, post_delete], sender=News)
@receiver([post_save, post_delete], sender=Rubric)
def clear_news_cache(sender, instance, **kwargs):
    clear_cache_by_prefix('index')
    clear_cache_by_prefix('news')
    clear_cache_by_prefix('news_single')


@receiver([post_save, post_delete], sender=Partner)
def clear_index_cache(sender, instance, **kwargs):
    clear_cache_by_prefix('index')
