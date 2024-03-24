from .models import News
from .admin import NewsAdmin
from .templatetags.e5_app_extras import show_list
from django.test import TestCase
from django.utils import timezone
from django.contrib.admin.sites import AdminSite
from django.conf import settings
import tempfile


class NewsAdminTest(TestCase):
    def test_get_description(self):
        news_created_at = timezone.now()
        news_slug_url = 'news-slag-test'
        news_description_short = 'test description'
        news = News.objects.create(created_at=news_created_at, slug_url=news_slug_url,
                                   description=news_description_short)
        self.assertEqual(NewsAdmin(model=News, admin_site=AdminSite()).get_description(news), news_description_short)
        news_description_long = '''test description test description test description test description test 
        description test description test description test description test description test description'''
        news.description = news_description_long
        self.assertEqual(NewsAdmin(model=News, admin_site=AdminSite()).get_description(news),
                         news_description_long[:30] + '...')

    def test_get_image(self):
        news_created_at = timezone.now()
        news_slug_url = 'news-slag-test'
        news = News.objects.create(created_at=news_created_at, slug_url=news_slug_url)
        self.assertEqual(NewsAdmin(model=News, admin_site=AdminSite()).get_image(news),
                         f'<img src="{settings.STATIC_URL}e5_app/frontend/images/news_default.png" width="50"/>')
        news.picture = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.assertEqual(NewsAdmin(model=News, admin_site=AdminSite()).get_image(news),
                         f'<img src = "{news.picture.url}" width = "50"/>')


class ExtrasTest(TestCase):
    def test_show_list(self):
        paragraph = 'tes\nparagraph'
        self.assertEqual({'lst': paragraph.split('\n')}, show_list(paragraph))
