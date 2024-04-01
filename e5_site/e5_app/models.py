from django.db import models
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail


class Common(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Rubric(Common):
    name = models.CharField(max_length=100, verbose_name='Название', )

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class News(Common):
    SHOW_CHOICES = {
        'a': 'Описание и картинка',
        'd': 'Описание',
        'p': 'Картинка',
        'e': 'Ничего'
    }
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание', )
    picture = models.ImageField(null=True, blank=True, upload_to='photos/news/%Y/%m', verbose_name='Картинка', )
    show = models.CharField(choices=SHOW_CHOICES, default='a', verbose_name='Отображать странице новости')
    content = RichTextUploadingField(null=True, blank=True, verbose_name='Дополнительная информация', )
    rubrics = models.ManyToManyField(Rubric, verbose_name='Рубрики' )
    created_at = models.DateTimeField(verbose_name='Дата создания', blank=True, db_index=True, )
    slug_url = models.SlugField(unique=True, verbose_name='Ссылка', )

    def get_absolute_url(self):
        return f'/site/news/{self.slug_url}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Employee(Common):
    photo = models.ImageField(upload_to='photos/employee/', verbose_name='Фото', )
    name = models.CharField(max_length=150, verbose_name='Имя', )
    description = models.TextField(null=True, blank=True, verbose_name='Информация', )
    email_first = models.EmailField(null=True, blank=True, max_length=50, verbose_name='Первая почта', )
    email_second = models.EmailField(null=True, blank=True, max_length=50, verbose_name='Вторая почта', )

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class WComponent(Common):
    name = models.CharField(max_length=150, verbose_name='Название', )

    class Meta:
        verbose_name = 'Свойство разработок'
        verbose_name_plural = 'Свойства разработок'


class Work(Common):
    photo = models.ImageField(upload_to='photos/works/', verbose_name='Фото', )
    name = models.CharField(max_length=150, verbose_name='Название', )
    description = models.TextField(null=True, blank=True, verbose_name='Описание', )
    components = models.ManyToManyField(WComponent, through='WorkComponent',
                                        through_fields=('work', 'component',), )

    class Meta:
        verbose_name = 'Разработка'
        verbose_name_plural = 'Разработки'


class WorkComponent(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name='Разработка', )
    component = models.ForeignKey(WComponent, on_delete=models.CASCADE, verbose_name='Свойство', )
    filling = models.TextField(null=True, blank=True, verbose_name='Заполнение', )

    def __str__(self):
        return 'Разработка-Свойство'

    def __repr__(self):
        return 'Разработка-Свойство'


class Company(Common):
    name = models.CharField(max_length=100, verbose_name='Название', db_index=True)
    photo = models.ImageField(upload_to='photos/companies/', verbose_name='Фото', )
    description = models.TextField(null=True, blank=True, verbose_name='Описание', )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['name']


class VComponent(Common):
    name = models.CharField(max_length=150, verbose_name='Название', )

    class Meta:
        verbose_name = 'Свойство вакансий'
        verbose_name_plural = 'Свойства вакансий'


class Vacancy(Common):
    name = models.CharField(max_length=150, verbose_name='Название', )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания' )
    salary = models.CharField(null=True, blank=True, max_length=100, verbose_name='Заработная плата', )
    experience = models.CharField(null=True, blank=True, max_length=100, verbose_name='Опыт работы', )
    schedule = models.CharField(null=True, blank=True, max_length=100, verbose_name='График труда', )
    slug_url = models.SlugField(unique=True, verbose_name='Ссылка', )
    content = RichTextUploadingField(null=True, blank=True, verbose_name='Дополнительная информация', )
    components = models.ManyToManyField(VComponent, through='VacancyComponent',
                                        through_fields=('vacancy', 'component',), )

    def get_absolute_url(self):
        return f'/site/vacancy/{self.slug_url}'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['pk']


class VacancyComponent(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name='Вакансия', )
    component = models.ForeignKey(VComponent, on_delete=models.CASCADE, verbose_name='Свойство', )
    filling = models.TextField(null=True, blank=True, verbose_name='Заполнение', )

    def __str__(self):
        return 'Вакансия-Свойство'

    def __repr__(self):
        return 'Вакансия-Свойство'


class Partner(Common):
    name = models.CharField(max_length=150, verbose_name='Название', db_index=True)
    photo = models.ImageField(upload_to='photos/partners/', verbose_name='Фото', )

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['name']


class EventType(Common):
    color = ColorField(unique=True, verbose_name='Цвет отображения', )

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'


class Event(Common):
    date = models.DateField(verbose_name='Дата', )
    info = models.TextField(null=True, blank=True, max_length=500, verbose_name='Дополнительно', )
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name='Тип мероприятия', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        mails = Mailing.objects.all()
        send_mail(f'Новое мероприятие Э5 {self.date}', f'{self.event_type.name}, {self.info}',
                  'mrusipusi@gmail.com', list(mails))

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['date']


class EventSchedule(Common):
    name = None
    start = models.TimeField(verbose_name='Время начала', )
    end = models.TimeField(null=True, blank=True, verbose_name='Время конца', )
    place = models.CharField(max_length=100, null=True, blank=True, verbose_name='Место проведения', )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        output = str(self.start.strftime("%H:%M"))
        if self.end:
            output += f'-{self.end.strftime("%H:%M")}'
        if self.place:
            output += f' {self.place}'
        return output

    def __repr__(self):
        output = str(self.start.strftime("%H:%M"))
        if self.end:
            output += f'-{self.end.strftime("%H:%M")}'
        if self.place:
            output += f' {self.place}'
        return output


class Visitor(Common):
    STAND_CHOICES = {
        'ab': 'Абитуриент',
        '11': '11 класс',
        '10': '10 класс',
        'dr': 'Другое',
    }
    event = models.ForeignKey(EventSchedule, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100, )
    mail = models.EmailField()
    phone = PhoneNumberField()
    stand = models.CharField(choices=STAND_CHOICES, )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_mail(f'Запись на мероприятие Э5 {self.event.event}, {self.event.event.date}',
                  f'Здравствуйте {self.name}, вы были успешно запсаны на {self.event}',
                  'mrusipusi@gmail.com', [self.mail])

    class Meta:
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'


class Mailing(models.Model):
    mail = models.EmailField(unique=True, verbose_name='Почта')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.mail

    def __repr__(self):
        return self.mail


class HTMLPage(models.Model):
    url_name = models.CharField(unique=True, verbose_name='Название пути')
    content = models.TextField(verbose_name='Контент для поиска')
    verbose = models.CharField(verbose_name='Название страницы')

    @classmethod
    def update_or_create_page(cls, name_and_url, new_content):
        obj, created = cls.objects.get_or_create(url_name=name_and_url[1])
        obj.content = new_content
        obj.verbose = name_and_url[0]
        obj.save()
        return obj, created

    class Meta:
        verbose_name = 'Страница HTML'
        verbose_name_plural = 'Страницы HTML'

    def __str__(self):
        return self.url_name

    def __repr__(self):
        return self.url_name
