from django.core.mail import send_mail
from .celery import app


@app.task
def send_mail_submitting(mail):
    send_mail(f'Подписка на рассылку Э5',
              f'Здравствуйте спасибо за подписку на рассылку Э5',
              'mrusipusi@gmail.com', [mail])


@app.task
def send_mail_event(event_pk):
    from .models import Event, Mailing
    event = Event.objects.get(pk=event_pk)
    mails = Mailing.objects.all()
    send_mail(f'Новое мероприятие Э5 {event.date}', f'{event.event_type.name}, {event.info}',
              'mrusipusi@gmail.com', list(mails))


@app.task
def send_mail_visitor(visitor_pk):
    from .models import Visitor
    visitor = Visitor.objects.get(pk=visitor_pk)
    send_mail(f'Запись на мероприятие Э5 {visitor.event.event}, {visitor.event.event.date}',
              f'Здравствуйте {visitor.name}, вы были успешно запсаны на {visitor.event}',
              'mrusipusi@gmail.com', [visitor.mail])
