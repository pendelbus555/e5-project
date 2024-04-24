from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e5_site.settings')

app = Celery('e5_app', broker='redis://redis:6379/1', include=['e5_app.tasks'])

if __name__ == '__main__':
    app.start()
