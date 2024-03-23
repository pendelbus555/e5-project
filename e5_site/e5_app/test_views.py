from django.test import TestCase
from django.utils.text import slugify
from .models import *
import tempfile
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.templatetags.static import static
from datetime import timedelta
from django.urls import reverse
import datetime as dt
from django.http import HttpResponse


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


class NewsTest(TestCase):
    def test_without_ajax(self):
        Rubric.objects.create()
        news_1_created_at = timezone.now() - timedelta(days=2 * 365)
        news_1_slug_url = 'news_1'
        news_2_created_at = timezone.now() - timedelta(days=365)
        news_2_slug_url = 'news_2'
        news_3_created_at = timezone.now()
        news_3_slug_url = 'news_3'
        News.objects.create(created_at=news_1_created_at, slug_url=news_1_slug_url)
        News.objects.create(created_at=news_2_created_at, slug_url=news_2_slug_url)
        News.objects.create(created_at=news_3_created_at, slug_url=news_3_slug_url)
        response = self.client.get('/site/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/news.html')
        self.assertEqual(response.context["selected"], 0)
        self.assertEqual(len(response.context["rubrics"]), 1)
        self.assertEqual(response.context["form"]['start_date'].value(),
                         news_1_created_at.replace(day=1).strftime('%Y-%m-%d'))
        self.assertEqual(response.context["form"]['end_date'].value(),
                         news_3_created_at.replace(day=1).strftime('%Y-%m-%d'))

    def test_with_ajax(self):
        rubric_1_name = 'Test rubric_1 name'
        rubric_1 = Rubric.objects.create(name=rubric_1_name)
        rubric_2_name = 'Test rubric_2 name'
        rubric_2 = Rubric.objects.create(name=rubric_2_name)
        news_1_created_at = timezone.now()
        news_2_created_at = timezone.now() - timedelta(days=365)
        news_1_name = 'Test news_1 name'
        news_2_name = 'Test news_2 name'
        news_1_slug_url = 'news_1'
        news_2_slug_url = 'news_2'
        news_1 = News.objects.create(name=news_1_name, slug_url=news_1_slug_url, created_at=news_1_created_at)
        news_1.rubrics.add(rubric_1)
        news_2 = News.objects.create(name=news_2_name, slug_url=news_2_slug_url, created_at=news_2_created_at)
        news_2.rubrics.add(rubric_2)

        response = self.client.get(path='/site/news/',
                                   headers={'X-Requested-With': 'XMLHttpRequest'},
                                   data={'page': '1', 'segment': 'news'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()['total_pages'], 1)
        data_news = response.json()['data_news']
        self.assertEqual(len(data_news), 2)
        self.assertEqual(data_news[0]['name'], news_1_name)
        self.assertEqual(parse_datetime(data_news[0]['created_at']).replace(microsecond=0),
                         news_1_created_at.replace(microsecond=0))
        self.assertEqual(data_news[0]['slug_url'], news_1_slug_url)

        response = self.client.get(path=reverse('news_rubric', kwargs={'rubric': rubric_2.pk}),
                                   headers={'X-Requested-With': 'XMLHttpRequest'},
                                   data={'page': '1', 'segment': str(rubric_2.pk)})
        self.assertEqual(response.json()['total_pages'], 1)
        data_news = response.json()['data_news']
        self.assertEqual(len(data_news), 1)
        self.assertEqual(data_news[0]['name'], news_2_name)


class NewsFilterTest(TestCase):
    def test_get(self):
        news_created_at = timezone.now()
        news_slug_url = 'news_1'
        News.objects.create(created_at=news_created_at, slug_url=news_slug_url)
        response = self.client.get(reverse('news_filter'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('news'))

    def test_post(self):
        news_1_created_at = timezone.now() - timedelta(days=2 * 365)
        news_1_slug_url = 'news_1'
        news_2_created_at = timezone.now() - timedelta(days=365)
        news_2_slug_url = 'news_2'
        news_3_created_at = timezone.now()
        news_3_slug_url = 'news_3'
        News.objects.create(created_at=news_1_created_at, slug_url=news_1_slug_url)
        News.objects.create(created_at=news_2_created_at, slug_url=news_2_slug_url)
        News.objects.create(created_at=news_3_created_at, slug_url=news_3_slug_url)
        response_start_date = news_3_created_at.strftime('%Y-%m')
        response_end_date = news_2_created_at.strftime('%Y-%m')
        response = self.client.post(reverse('news_filter'), {'start_date': response_start_date,
                                                             'end_date': response_end_date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/news_filter.html')

        self.assertEqual(len(response.context['filtered_news']), 2)
        self.assertEqual(response.context['filtered_news'][0].slug_url, 'news_3')
        self.assertEqual(response.context['filtered_news'][1].slug_url, 'news_2')


class NewsSingleTest(TestCase):
    def test_get(self):
        news_1_created_at = timezone.now() - timedelta(days=2 * 365)
        news_1_slug_url = 'news_1'
        news_2_created_at = timezone.now() - timedelta(days=365)
        news_2_slug_url = 'news_2'
        news_3_created_at = timezone.now()
        news_3_slug_url = 'news_3'
        News.objects.create(created_at=news_1_created_at, slug_url=news_1_slug_url)
        News.objects.create(created_at=news_2_created_at, slug_url=news_2_slug_url)
        News.objects.create(created_at=news_3_created_at, slug_url=news_3_slug_url)
        response = self.client.get(reverse('news_single', kwargs={'slug': news_2_slug_url}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/news_single.html')
        self.assertEqual(len(response.context["last_news"]), 3)
        self.assertEqual(response.context["news_single"].slug_url, news_2_slug_url)
        self.assertEqual(response.context["news_before"].slug_url, news_1_slug_url)
        self.assertEqual(response.context["news_after"].slug_url, news_3_slug_url)


class ScheduleTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/schedule.html')
        self.assertIn('week', response.context)
        self.assertEqual(response.context['week'], dt.date.today().isocalendar()[1] - 5)


class VacancyDetailViewTest(TestCase):
    def test_get_context_data(self):
        vacancy_2_slug_url = 'vacancy_2'
        company_photo = tempfile.NamedTemporaryFile(suffix=".jpg").name
        company = Company.objects.create(photo=company_photo)
        Vacancy.objects.create(pk=2, slug_url=vacancy_2_slug_url, company=company, )
        response = self.client.get(reverse('vacancy_single', kwargs={'slug': vacancy_2_slug_url}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/vacancy_single.html')
        self.assertEqual(response.context['vacancy'].slug_url, vacancy_2_slug_url)
        self.assertEqual(response.context['vacancy_before'], None)
        self.assertEqual(response.context['vacancy_after'], None)
        vacancy_1_slug_url = 'vacancy_1'
        Vacancy.objects.create(pk=1, slug_url=vacancy_1_slug_url, company=company, )
        vacancy_3_slug_url = 'vacancy_3'
        Vacancy.objects.create(pk=3, slug_url=vacancy_3_slug_url, company=company, )
        response = self.client.get(reverse('vacancy_single', kwargs={'slug': vacancy_2_slug_url}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['vacancy'].slug_url, vacancy_2_slug_url)
        self.assertEqual(response.context['vacancy_before'].slug_url, vacancy_1_slug_url)
        self.assertEqual(response.context['vacancy_after'].slug_url, vacancy_3_slug_url)


class SearchTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_post(self):
        search = 'Test search name'
        company = Company.objects.create()
        news = News.objects.create(name=search, created_at=timezone.now(), slug_url='news_1')
        vacancy = Vacancy.objects.create(name=search, company=company, slug_url='vacancy_1')
        HTMLPage.update_or_create_page(url_name='works', new_content='')
        Work.objects.create(name=search)
        response = self.client.post(reverse('search'), {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/search.html')
        self.assertEqual(response.context['search_text'], search)
        self.assertEqual(response.context['news_list'][0], news)
        self.assertEqual(response.context['vacancy_list'][0], vacancy)
        self.assertEqual(response.context['page_list'][0].url_name, 'works')


class EventListViewTest(TestCase):
    def test_get_context_data(self):
        event_type = EventType.objects.create()
        event_date = timezone.now()
        event = Event.objects.create(date=event_date, event_type=event_type)
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertTemplateUsed(response, 'e5_app/events.html')
        self.assertEqual(response.context['event_list'][0], event)
        self.assertIn('mailing_form', response.context)

    def test_without_ajax(self):
        event_type = EventType.objects.create()
        event_date = timezone.now()
        event = Event.objects.create(date=event_date, event_type=event_type, name='Test event name')
        EventSchedule.objects.create(event=event, start=timezone.now().time())
        response = self.client.get(reverse('events'), headers={'Event': event.pk})
        self.assertIn('form', response.context)

    def test_with_ajax_mailing(self):
        mail = 'test@test.test'
        response = self.client.post(reverse('events'), {'submit_mailing': True, 'mail': mail},
                                    headers={'HX-Boosted': True})
        self.assertIsInstance(response, HttpResponse)
        self.assertContains(response, 'Подписка успешно оформлена!')
        self.assertEqual(len(Mailing.objects.all()), 1)
        response = self.client.post(reverse('events'), {'submit_mailing': True, 'mail': mail},
                                    headers={'HX-Boosted': True})
        self.assertIsInstance(response, HttpResponse)
        self.assertContains(response, 'Данная почта уже подписана на рассылку')

    def test_with_ajax_visitor(self):
        event_type = EventType.objects.create()
        event_date = timezone.now()
        event = Event.objects.create(date=event_date, event_type=event_type, name='Test event name')
        event_schedule = EventSchedule.objects.create(event=event, start=timezone.now().time())
        response = self.client.post(reverse('events'),
                                    {
                                        'submit_visitor': True,
                                        'event': event_schedule.pk,
                                        'name': 'test test test',
                                        'mail': 'test@test.test',
                                        'phone': '+79774235467',
                                        'stand': '11',
                                    },
                                    headers={'HX-Boosted': True})
        self.assertIsInstance(response, HttpResponse)
        self.assertContains(response, 'Запись принята!')
        self.assertEqual(len(Visitor.objects.all()), 1)
        response = self.client.post(reverse('events'),
                                    {
                                        'submit_visitor': True,
                                        'event': event_schedule.pk,
                                        'name': 'test test test',
                                        'mail': 'test@test.test',
                                        'phone': 'error phone',
                                        'stand': '11',
                                    },
                                    headers={'HX-Boosted': True})
        self.assertIsInstance(response, HttpResponse)
        self.assertIn('HX-Retarget', response)

