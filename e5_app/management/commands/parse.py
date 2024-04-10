from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
from django.template.loader import get_template
import re
from e5_app.models import HTMLPage
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Parse html pages to index'

    def handle(self, *args, **options):
        templates = {
            'e5_app/index.html': ['Главная', 'index'],
            'e5_app/news.html': ['Новости', 'news'],
            'e5_app/history.html': ['История кафедры', 'history'],
            'e5_app/directions.html': ['Основные направления развития', 'directions'],
            'e5_app/programs.html': ['Учебные программы курсов', 'programs'],
            'e5_app/plan.html': ['Рабочий учебный план', 'plan'],
            'e5_app/schedule.html': ['Расписание', 'schedule'],
            'e5_app/contacts.html': ['Контакты', 'contacts'],
            'e5_app/employees.html': ['Преподаватели', 'employees'],
            'e5_app/works.html': ['Наши разработки', 'works'],
            'e5_app/vacancy.html': ['Вакансии', 'vacancy'],
            'e5_app/events.html': ['Мероприятия', 'events'],
        }

        for template, name_and_url in templates.items():
            template = get_template(template)
            with open(template.origin.name, 'r') as file:
                template_content = file.read()
            soup = BeautifulSoup(template_content, 'html.parser')
            cleaned_text = ''
            for string in soup.stripped_strings:
                text_without_n = string.replace('\n', '')
                text_without_tags = re.sub(r'{%.*?%}', '', text_without_n)
                text_without_vars = re.sub(r'{{.*?}}', '', text_without_tags)
                text_without_spaces = re.sub(r'\s+', ' ', text_without_vars)
                if len(text_without_spaces) >= 2:
                    cleaned_text += text_without_spaces + '\n'
            HTMLPage.update_or_create_page(name_and_url=name_and_url, new_content=cleaned_text)
