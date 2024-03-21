from django.test import TestCase
from django.utils.text import slugify
from .models import *
import tempfile
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.templatetags.static import static


class IndexTest(TestCase):
    def test_without_ajax(self):
        partner_photo = tempfile.NamedTemporaryFile(suffix=".jpg").name
        Partner.objects.create(photo=partner_photo)
        response = self.client.get('/site/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/index.html')
        self.assertEqual(len(response.context["partners"]), 1)

    def test_with_ajax_news(self):
        news_name = 'Test news name'
        news_picture = tempfile.NamedTemporaryFile(suffix=".jpg").name
        news_description = 'Test news description'
        news_created_at = timezone.now()
        news_content = 'Test news content'
        news_slug_url = slugify(news_name)
        rubric = Rubric.objects.create()
        news = News.objects.create(
            name=news_name,
            picture=news_picture,
            description=news_description,
            created_at=news_created_at,
            content=news_content,
            slug_url=news_slug_url,
        )
        news.rubrics.add(rubric)
        response = self.client.get(path='/site/',
                                   headers={'X-Requested-With': 'XMLHttpRequest'},
                                   data={'from': 'news', 'page': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()['total_pages'], 1)
        data_news = response.json()['data_news'][0]
        self.assertEqual(len(data_news), 5)
        self.assertEqual(data_news['name'], news_name)
        self.assertEqual(data_news['description'], news_description)
        self.assertEqual(parse_datetime(data_news['created_at']).replace(microsecond=0),
                         news_created_at.replace(microsecond=0))
        self.assertEqual(data_news['slug_url'], news_slug_url)
        self.assertEqual(data_news['picture_url'], f'/media{news_picture}')
        news.picture = None
        news.save()
        response = self.client.get(path='/site/',
                                   headers={'X-Requested-With': 'XMLHttpRequest'},
                                   data={'from': 'news', 'page': '1'})
        self.assertEqual(response.json()['data_news'][0]['picture_url'],
                         static('e5_app/frontend/images/news_default.png'))

    def test_with_ajax_vacancy(self):
        company_name = 'Test company name'
        vacancy_name = 'Test vacancy name'
        vacancy_slug_url = slugify(vacancy_name)
        vacancy_salary = 'Test vacancy salary'
        company = Company.objects.create(name=company_name)
        Vacancy.objects.create(name=vacancy_name, slug_url=vacancy_slug_url, company=company,
                               salary=vacancy_salary)
        response = self.client.get(path='/site/',
                                   headers={'X-Requested-With': 'XMLHttpRequest'},
                                   data={'from': 'vacancy', 'page': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()), 2)
        data_vacancy = response.json()['data_vacancy'][0]
        self.assertEqual(len(data_vacancy), 4)
        self.assertEqual(data_vacancy['name'], vacancy_name)
        self.assertEqual(data_vacancy['salary'], vacancy_salary)
        self.assertEqual(data_vacancy['company_name'], company_name)
        self.assertEqual(data_vacancy['slug_url'], vacancy_slug_url)
