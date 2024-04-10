from django.test import TestCase
from .models import *
from django.utils.text import slugify
from django.utils import timezone
from django.core import mail


class CommonTest(TestCase):
    def test_repr_str(self):
        rubric_name = 'Test rubric name'
        rubric = Rubric.objects.create(name=rubric_name)
        self.assertEqual(repr(rubric), rubric_name, 'Common __repr__ method do not return name')
        self.assertEqual(str(rubric), rubric_name, 'Common __str__ method do not return name')


class NewsTest(TestCase):
    def test_absolute_url(self):
        news_name = 'Test news name'
        news_slug_url = 'test-news-name'
        news_created_at = timezone.now()
        news = News.objects.create(name=news_name, created_at=news_created_at, slug_url=news_slug_url, )
        url = news.get_absolute_url()
        self.assertTrue(url, 'News do not have absolute url')
        self.assertEqual(url, f'/site/news/{slugify(news_name)}', 'News have wrong absolute url')


class VacancyTest(TestCase):
    def test_absolute_url(self):
        vacancy_name = 'Test vacancy name'
        vacancy_slug_url = slugify(vacancy_name)
        company_name = 'Test company name'
        company = Company.objects.create(name=company_name)
        vacancy = Vacancy.objects.create(name=vacancy_name, slug_url=vacancy_slug_url, company=company)
        url = vacancy.get_absolute_url()
        self.assertTrue(url, 'Vacancy do not have absolute url')
        self.assertEqual(url, f'/site/vacancy/{vacancy_slug_url}', 'Vacancy have wrong absolute url')


class WorkComponentTest(TestCase):
    def test_repr_str(self):
        work_name = 'Test work name'
        w_component_name = 'Test w_component name'
        work = Work.objects.create(name=work_name)
        w_component = WComponent.objects.create(name=w_component_name)
        work_component_repr_str = 'Разработка-Свойство'
        work_component = WorkComponent.objects.create(work=work, component=w_component)
        self.assertEqual(repr(work_component), work_component_repr_str,
                         'WorkComponent __repr__ method do not return name')
        self.assertEqual(str(work_component), work_component_repr_str,
                         'WorkComponent __str__ method do not return name')


class VacancyComponentTest(TestCase):
    def test_repr_str(self):
        vacancy_name = 'Test vacancy name'
        v_component_name = 'Test v_component name'
        company_name = 'Test company name'
        company = Company.objects.create(name=company_name)
        vacancy = Vacancy.objects.create(name=vacancy_name, company=company)
        v_component = VComponent.objects.create(name=v_component_name)
        vacancy_component_repr_str = 'Вакансия-Свойство'
        vacancy_component = VacancyComponent.objects.create(vacancy=vacancy, component=v_component)
        self.assertEqual(repr(vacancy_component), vacancy_component_repr_str,
                         'VacancyComponent __repr__ method do not return name')
        self.assertEqual(str(vacancy_component), vacancy_component_repr_str,
                         'VacancyComponent __str__ method do not return name')


class MailingTest(TestCase):
    def test_repr_str(self):
        mail = 'test@test.test'
        mailing = Mailing.objects.create(mail=mail)
        self.assertEqual(repr(mailing), mail, 'Mailing __repr__ method do not return name')
        self.assertEqual(str(mailing), mail, 'Mailing __str__ method do not return name')


class HTMLPageTest(TestCase):
    def test_repr_str(self):
        html_page_url_name = 'test'
        html_page = HTMLPage.objects.create(url_name=html_page_url_name)
        self.assertEqual(repr(html_page), html_page_url_name, 'HTMLPage __repr__ method do not return name')
        self.assertEqual(str(html_page), html_page_url_name, 'HTMLPage __str__ method do not return name')

    def test_update_or_create_page(self):
        html_page_url_name = 'test'
        html_page_content_old = 'Test html_page content old'
        html_page_content_new = 'Test html_page content new'
        HTMLPage.update_or_create_page(url_name=html_page_url_name, new_content=html_page_content_old)
        html_page = HTMLPage.objects.get(url_name=html_page_url_name)
        self.assertEqual(html_page.content, html_page_content_old, 'Content was not delivered')
        HTMLPage.update_or_create_page(url_name=html_page_url_name, new_content=html_page_content_new)
        html_page = HTMLPage.objects.get(url_name=html_page_url_name)
        self.assertEqual(html_page.content, html_page_content_new, 'Content was not changed')


class EventTest(TestCase):
    def test_save(self):
        mailing_mail = 'test@test.test'
        event_type = EventType.objects.create()
        Mailing.objects.create(mail=mailing_mail)
        event_date = timezone.now()
        Event.objects.create(date=event_date, event_type=event_type)
        self.assertEqual(len(mail.outbox), 1, 'Message was not delivered')
        self.assertEqual(mail.outbox[0].subject, f'Новое мероприятие Э5 {event_date}',
                         'Message subject is not correct')


class EventScheduleTest(TestCase):
    def test_repr_str(self):
        event_type = EventType.objects.create()
        event_date = timezone.now()
        event_schedule_start = timezone.now().time()
        event_schedule_end = (timezone.now() + timezone.timedelta(hours=1)).time()
        event_schedule_place = 'Test event_schedule place'
        event = Event.objects.create(date=event_date, event_type=event_type)
        event_schedule = EventSchedule.objects.create(event=event,
                                                      start=event_schedule_start,
                                                      end=event_schedule_end,
                                                      place=event_schedule_place, )
        self.assertEqual(
            repr(event_schedule),
            str(event_schedule_start.strftime("%H:%M")) + '-' + str(
                event_schedule_end.strftime("%H:%M")) + ' ' + event_schedule_place,
            'EventSchedule __repr__ method do not return name'
        )
        self.assertEqual(
            str(event_schedule),
            str(event_schedule_start.strftime("%H:%M")) + '-' + str(
                event_schedule_end.strftime("%H:%M")) + ' ' + event_schedule_place,
            'EventSchedule __str__ method do not return name'
        )


class VisitorTest(TestCase):
    def test_save(self):
        event_type = EventType.objects.create()
        event_name = 'Test event name'
        event_date = timezone.now()
        event_schedule_start = timezone.now().time()
        visitor_mail = 'test@test.test'
        event_schedule_end = (timezone.now() + timezone.timedelta(hours=1)).time()
        event = Event.objects.create(name=event_name, event_type=event_type, date=event_date)
        event_schedule = EventSchedule.objects.create(event=event,
                                                      start=event_schedule_start,
                                                      end=event_schedule_end, )
        Visitor.objects.create(event=event_schedule, mail=visitor_mail)
        self.assertEqual(len(mail.outbox), 1, 'Message was not delivered')
        self.assertEqual(
            mail.outbox[0].subject,
            f'Запись на мероприятие Э5 {event_name}, {event_date}',
            'Message subject is not correct'
        )
