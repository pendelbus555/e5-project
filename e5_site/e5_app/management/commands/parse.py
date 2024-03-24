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
            'e5_app/index.html': 'index',
            'e5_app/news.html': 'news',
            'e5_app/history.html': 'history',
            'e5_app/directions.html': 'directions',
            'e5_app/programs.html': 'programs',
            'e5_app/plan.html': 'plan',
            'e5_app/schedule.html': 'schedule',
            'e5_app/contacts.html': 'contacts',
            'e5_app/employees.html': 'employees',
            'e5_app/works.html': 'works',
            'e5_app/vacancy.html': 'vacancy',
            'e5_app/events.html': 'events',
        }

        for template, url_name in templates.items():
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
            HTMLPage.update_or_create_page(url_name=url_name, new_content=cleaned_text)
