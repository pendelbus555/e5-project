from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
from django.template.loader import get_template
import re
from e5_app.models import HTMLPage


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
            with open(template.origin.name, 'r', encoding='utf-8') as file:
                cleaned_text = strip_tags(file.read())
                cleaned_text = re.sub(r'{%\s*.*?\s*%}', '', cleaned_text, flags=re.DOTALL)
                cleaned_text = re.sub(r'^var\s+\w+\s*=\s*.*?;', '', cleaned_text,
                                      flags=re.MULTILINE)
                cleaned_text = re.sub(r'^&\w+.*?;', '', cleaned_text,
                                      flags=re.MULTILINE)
                cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
                cleaned_text = re.sub(r'const\s+data\s*=\s*document.currentScript.dataset;.*?render\(\);', '', cleaned_text,
                                      flags=re.DOTALL)
                cleaned_text = re.sub(r'{{.*?}}', '', cleaned_text)
                cleaned_text = re.sub(r'^\s+|\s+$', '', cleaned_text, flags=re.MULTILINE)
                cleaned_text = cleaned_text.lower()
            HTMLPage.update_or_create_page(url_name=url_name, new_content=cleaned_text)
