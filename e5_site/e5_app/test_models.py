from django.test import TestCase
from .models import *
from django.utils.text import slugify
from django.utils import timezone


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
        news = News.objects.create(name=news_name, created_at=timezone.now(), slug_url=news_slug_url, )
        url = news.get_absolute_url()
        self.assertTrue(url, 'News do not have absolute url')
        self.assertEqual(url, f'/site/news/{slugify(news_name)}', 'News have wrong absolute url')


class VacancyTest(TestCase):
    def test_absolute_url(self):
        vacancy_name = 'Test vacancy name'
        vacancy_slug_url = 'test-vacancy-name'
        company_name = 'Test company name'
        company = Company.objects.create(name=company_name)
        vacancy = Vacancy.objects.create(name=vacancy_name, slug_url=vacancy_slug_url, company=company)
        url = vacancy.get_absolute_url()
        self.assertTrue(url, 'Vacancy do not have absolute url')
        self.assertEqual(url, f'/site/vacancy/{slugify(vacancy_name)}', 'Vacancy have wrong absolute url')


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
