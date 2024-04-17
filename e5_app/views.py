import django.db
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import News, Rubric, Employee, Work, Vacancy, Partner, Event, Mailing, EventSchedule, Visitor, HTMLPage
from .forms import NewsFilterForm, MailingForm, VisitorForm
import calendar
import datetime as dt
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.templatetags.static import static
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from django.contrib.postgres.search import SearchVector
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils.text import Truncator
from django.core.paginator import Paginator


def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        per_page = 4

        # Take additional headers to distinguish ajax
        request_type = request.headers.get('From')

        if request_type == 'news':
            queryset = News.objects.only(
                'name', 'description', 'created_at', 'slug_url', 'picture')

            def serializer(obj): return {
                'name': obj.name,
                'description': Truncator(obj.description).words(20),
                'created_at': obj.created_at.strftime('%d.%m.%Y'),
                'slug_url': obj.slug_url,
                # Take picture from static if it doesn't exist
                'picture_url': obj.picture.url if obj.picture else static('e5_app/frontend/images/news_default.png')
            }
        elif request_type == 'vacancy':
            queryset = Vacancy.objects.only(
                'name', 'salary', 'company__name', 'slug_url').select_related('company')

            def serializer(obj): return {
                'name': obj.name.upper(),
                'salary': obj.salary.lower() if obj.salary else None,
                'company_name': obj.company.name,
                'slug_url': obj.slug_url
            }

        paginator = Paginator(queryset, per_page)
        page_data = paginator.page(page)

        serialized_data = [serializer(obj) for obj in page_data]
        total_pages = paginator.num_pages

        return JsonResponse({'data': serialized_data, 'total_pages': total_pages})
    else:
        # If not ajax request - check for some models existing
        partners = Partner.objects.all()
        ctx = {'partners': partners, }

        if not partners.exists():
            ctx.update({'message_partners': 'Партнеров нет'})
        if not News.objects.exists():
            ctx.update({'message_news': 'Новостей нет'})
        if not Vacancy.objects.exists():
            ctx.update({'message_vacancy': 'Вакансий нет'})

        return render(request, 'e5_app/index.html', ctx)


def news(request, rubric=0):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        segment = request.GET.get('segment')

        # If the segment is 'news' - take all news, else - convert 
        # segment to integer and filter news by rubric pk
        if segment == 'news':
            queryset = News.objects.only('name', 'created_at', 'slug_url')
        else:
            queryset = News.objects.filter(rubrics__pk=int(
                segment)).only('name', 'created_at', 'slug_url')

        def serializer(obj): return {
            'name': obj.name,
            'created_at': obj.created_at.strftime("%d.%m.%Y %H:%M"),
            'slug_url': obj.slug_url,
        }

        per_page = 10
        paginator = Paginator(queryset, per_page)
        page_data = paginator.page(page)

        serialized_data = [serializer(obj) for obj in page_data]
        total_pages = paginator.num_pages

        return JsonResponse({'data_news': serialized_data, 'total_pages': total_pages})
    else:
        # If not ajax request - check for some models existing
        # and create filter form with boundary dates
        rubrics = Rubric.objects.all()
        news = News.objects.only('name', 'created_at', 'slug_url')
        if not news.exists():
            return render(request, 'e5_app/news.html', {'rubrics': rubrics, 'message': 'Новостей нет'})

        min_date = News.objects.only('created_at').earliest(
            'created_at').created_at.replace(day=1).strftime('%Y-%m-%d')
        max_date = News.objects.only('created_at').latest(
            'created_at').created_at.replace(day=1).strftime('%Y-%m-%d')

        form = NewsFilterForm(min_date=min_date, max_date=max_date)

        return render(request, 'e5_app/news.html', {'rubrics': rubrics, 'selected': rubric, 'form': form})


def news_filter(request):
    if request.method == 'POST':
        # Absorb News boundary dates
        min_date = News.objects.only('created_at').earliest(
            'created_at').created_at.replace(day=1).strftime('%Y-%m-%d')
        max_date = News.objects.only('created_at').latest(
            'created_at').created_at.replace(day=1).strftime('%Y-%m-%d')

        form = NewsFilterForm(
            request.POST, min_date=min_date, max_date=max_date)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Change for increasing if neeeded
            if end_date < start_date:
                start_date, end_date = end_date, start_date

            # For start month replace day with 1
            # For end month replace day with last day of the month
            start_date = start_date.replace(day=1)
            end_date = end_date.replace(
                day=calendar.monthrange(end_date.year, end_date.month)[1])

            # Also add time for dates
            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())

            # Include TIMEZONES! 
            start_date = make_aware(start_date)
            end_date = make_aware(end_date)

            filtered_news = News.objects.filter(created_at__range=[start_date, end_date]).only('name', 'created_at',
                                                                                               'slug_url')

            return render(request, 'e5_app/news_filter.html',
                          {'form': form, 'start_date': start_date, 'end_date': end_date,
                           'filtered_news': filtered_news, })
    else:
        return redirect('news')


def news_single(request, slug):
    rubrics = Rubric.objects.all()

    news_single_obj = News.objects.get(slug_url=slug)

    news_before = News.objects.only('name', 'slug_url').filter(created_at__lt=news_single_obj.created_at).order_by(
        '-created_at').first()
    news_after = News.objects.only('name', 'slug_url').filter(created_at__gt=news_single_obj.created_at).order_by(
        'created_at').first()

    last_news = News.objects.only('name', 'created_at', 'slug_url')[:5]

    return render(request, 'e5_app/news_single.html',
                  {'rubrics': rubrics, 'news_single': news_single_obj, 'last_news': last_news,
                   'news_before': news_before, 'news_after': news_after})


class HistoryView(TemplateView):
    template_name = 'e5_app/history.html'


class DirectionsView(TemplateView):
    template_name = 'e5_app/directions.html'


class ProgramsView(TemplateView):
    template_name = 'e5_app/programs.html'


class PlanView(TemplateView):
    template_name = 'e5_app/plan.html'


def schedule(request):
    # Absorb week's number of year
    today = dt.date.today()
    week = today.isocalendar()[1]

    ctx = {'week': week - 5}

    return render(request, 'e5_app/schedule.html', context=ctx)


class ContactsView(TemplateView):
    template_name = 'e5_app/contacts.html'


class EmployeesListView(ListView):
    model = Employee
    context_object_name = "employees_list"
    template_name = "e5_app/employees.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        for employee in queryset:
            employee.name = employee.name.split()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not super().get_queryset().exists():
            context['message'] = 'Сотрудников нет'

        return context


class WorkListView(ListView):
    model = Work
    context_object_name = 'work_list'
    template_name = 'e5_app/works.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("workcomponent_set__component")

        if not queryset.exists():
            self.extra_context = {'message': 'Разработок нет'}

        return queryset


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'e5_app/vacancy.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('company').only(
            'name', 'salary', 'company__name', 'experience', 'schedule', 'slug_url')

        if not queryset.exists():
            self.extra_context['message'] = 'Вакансий нет'

        return queryset


class VacancyDetailView(DetailView):
    model = Vacancy
    slug_field = 'slug_url'
    context_object_name = 'vacancy'
    template_name = 'e5_app/vacancy_single.html'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('company').prefetch_related(
            "vacancycomponent_set__component")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        obj = self.object

        vacancy_before = Vacancy.objects.only(
            'name', 'slug_url').filter(pk__lt=obj.pk).first()
        vacancy_after = Vacancy.objects.only(
            'name', 'slug_url').filter(pk__gt=obj.pk).first()

        context['vacancy_before'] = vacancy_before
        context['vacancy_after'] = vacancy_after

        return context


class EventListView(ListView):
    model = Event
    context_object_name = 'event_list'
    template_name = 'e5_app/events.html'
    extra_context = {'mailing_form': MailingForm()}

    def get_queryset(self):
        queryset = super().get_queryset()

        if not queryset.exists():
            self.extra_context['message'] = 'Мероприятий нет'

        return queryset

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        # Distinquish htmx ajax request
        if request.headers.get('HX-Boosted'):
            if 'submit_mailing' in request.POST:
                form = MailingForm(request.POST)

                if form.is_valid():
                    data = form.cleaned_data
                    try:
                        Mailing.objects.create(mail=data['mail'])
                        return HttpResponse('''<div class="text-success">
                                              Подписка успешно оформлена!</div>''')
                    except django.db.IntegrityError:
                        return HttpResponse('''<div class="text-warning">
                                              Данная почта уже подписана на рассылку</div>''')
            if 'submit_visitor' in request.POST:
                event_schedule_pk = int(request.POST.get('event'))
                form = VisitorForm(request.POST, event_pk=EventSchedule.objects.get(
                    pk=event_schedule_pk).event.pk)

                if form.is_valid():
                    data = form.cleaned_data
                    Visitor.objects.create(event=data['event'], name=data['name'], mail=data['mail'],
                                           phone=data['phone'], stand=data['stand'])
                    return HttpResponse('''<div class="text-success">
                                                                 Запись принята!</div>''')
                else:
                    # Show form errors
                    response = HttpResponse(str(form.errors))
                    response["HX-Retarget"] = "#visitor_errors"
                    return response
        elif request.headers.get('Event'):
            event_pk = int(request.headers.get('Event'))
            form = VisitorForm(event_pk=event_pk)

            ctx = {}
            ctx.update(csrf(request))

            form_html = render_crispy_form(form, context=ctx)

            return HttpResponse(form_html)

        return response


def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('search', None)

        # Start search with SearchVector with filter

        page_list = HTMLPage.objects.annotate(
            search=SearchVector("content"),
        ).filter(search=search_text)

        news_list = News.objects.annotate(
            search=SearchVector("name", "description",
                                "created_at", "content"),
        ).filter(search=search_text)

        vacancy_list = Vacancy.objects.annotate(
            search=SearchVector("name", "company__name",
                                "salary", "experience", "schedule", "content"),
        ).filter(search=search_text)

        works_list = Work.objects.annotate(
            search=SearchVector("name", "description"),
        ).filter(search=search_text)
        # Add works page if it is not in page_list, but Work objects searched
        if works_list and not page_list.filter(url_name='works'):
            page_list |= HTMLPage.objects.filter(url_name='works')

        employee_list = Employee.objects.annotate(
            search=SearchVector("name", "description"),
        ).filter(search=search_text)
        # Add empoyees page if it is not in page_list, but Employee objects searched
        if employee_list and not page_list.filter(url_name='employees'):
            page_list |= HTMLPage.objects.filter(url_name='employees')

        if not any([news_list, vacancy_list, page_list]):
            ctx = {'search_text': search_text, 'message': 'Ничего не найдено'}
        else:
            ctx = {'search_text': search_text, 'news_list': news_list, 'vacancy_list': vacancy_list,
                   'page_list': page_list}

        return render(request, 'e5_app/search.html', ctx)
    else:
        return redirect('index')
