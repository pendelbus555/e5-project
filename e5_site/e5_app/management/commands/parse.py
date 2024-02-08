from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Parse news from e5.bmstu.ru'

    def handle(self, *args, **options):
        print('hello world')
