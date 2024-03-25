import django.db
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import News, Rubric, Employee, Work, Vacancy, Partner, Event, Mailing, EventSchedule, Visitor, HTMLPage
import math
from .forms import NewsFilterForm, MailingForm, VisitorForm
from django.db.models import Min, Max
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


def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.GET.get('from') == 'news':
            page = int(request.GET.get('page'))
            per_page = 4
            starting_number = (page - 1) * per_page
            ending_number = page * per_page
            news = News.objects.all()[starting_number:ending_number]
            total_pages = math.ceil(News.objects.count() / per_page)
            serialized_news = []
            for n in news:
                news_data = {
                    'name': n.name,
                    'description': n.description,
                    'created_at': n.created_at,
                    'slug_url': n.slug_url
                }
                if n.picture:
                    news_data['picture_url'] = n.picture.url
                else:
                    news_data['picture_url'] = static('e5_app/frontend/images/news_default.png')
                serialized_news.append(news_data)

            return JsonResponse({'data_news': serialized_news, 'total_pages': total_pages})
        elif request.GET.get('from') == 'vacancy':
            page = int(request.GET.get('page'))
            per_page = 4
            starting_number = (page - 1) * per_page
            ending_number = page * per_page
            vacancy = Vacancy.objects.all()[starting_number:ending_number]
            total_pages = math.ceil(Vacancy.objects.count() / per_page)
            serialized_news = []
            for v in vacancy:
                vacancy_data = {
                    'name': v.name,
                    'salary': v.salary,
                    'company_name': v.company.name,
                    'slug_url': v.slug_url
                }
                serialized_news.append(vacancy_data)
            return JsonResponse({'data_vacancy': serialized_news, 'total_pages': total_pages})
    else:
        partners = Partner.objects.all()
        return render(request, 'e5_app/index.html', {'partners': partners, }, )


def news(request, rubric=0):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page'))
        segment = request.GET.get('segment')
        per_page = 10
        starting_number = (page - 1) * per_page
        ending_number = page * per_page
        if segment == 'news':
            news = News.objects.all()[starting_number:ending_number]
            total_pages = math.ceil(News.objects.count() / per_page)
        else:
            news = News.objects.all().filter(rubrics__pk=int(segment))[starting_number:ending_number]
            total_pages = math.ceil(News.objects.filter(rubrics__pk=int(segment)).count() / per_page)

        serialized_news = []
        for n in news:
            news_data = {
                'name': n.name,
                'created_at': n.created_at,
                'slug_url': n.slug_url
            }
            serialized_news.append(news_data)
        return JsonResponse({'data_news': serialized_news, 'total_pages': total_pages})
    else:
        rubrics = Rubric.objects.all()
        min_date = News.objects.aggregate(Min('created_at'))['created_at__min']
        max_date = News.objects.aggregate(Max('created_at'))['created_at__max']
        min_date = min_date.replace(day=1)
        max_date = max_date.replace(day=1)
        form = NewsFilterForm(min_date=min_date.strftime('%Y-%m-%d'), max_date=max_date.strftime('%Y-%m-%d'))
        return render(request, 'e5_app/news.html', {'rubrics': rubrics, 'selected': rubric, 'form': form})


def news_filter(request):
    if request.method == 'POST':
        min_date = News.objects.aggregate(Min('created_at'))['created_at__min']
        max_date = News.objects.aggregate(Max('created_at'))['created_at__max']
        min_date = min_date.replace(day=1)
        max_date = max_date.replace(day=1)
        form = NewsFilterForm(request.POST, min_date=min_date.strftime('%Y-%m-%d'),
                              max_date=max_date.strftime('%Y-%m-%d'))
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if end_date < start_date:
                start_date, end_date = end_date, start_date

            start_date = start_date.replace(day=1)
            end_date = end_date.replace(day=calendar.monthrange(end_date.year, end_date.month)[1])

            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())

            start_date = make_aware(start_date)
            end_date = make_aware(end_date)

            filtered_news = News.objects.filter(created_at__range=[start_date, end_date])

            return render(request, 'e5_app/news_filter.html',
                          {'form': form, 'start_date': start_date, 'end_date': end_date,
                           'filtered_news': filtered_news, })
    else:
        return redirect('news')


def news_single(request, slug):
    rubrics = Rubric.objects.all()
    news_single_obj = News.objects.get(slug_url=slug)
    news_before = News.objects.filter(created_at__lt=news_single_obj.created_at).order_by('-created_at').first()
    news_after = News.objects.filter(created_at__gt=news_single_obj.created_at).order_by('created_at').first()
    last_news = News.objects.all()[:5]
    print(news_single_obj, news_single_obj.content, news_single_obj.slug_url)
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


class WorkListView(ListView):
    model = Work
    context_object_name = 'work_list'
    template_name = 'e5_app/works.html'


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'e5_app/vacancy.html'


class VacancyDetailView(DetailView):
    model = Vacancy
    slug_field = 'slug_url'
    context_object_name = 'vacancy'
    template_name = 'e5_app/vacancy_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.get_object()
        try:
            vacancy_before = Vacancy.objects.get(pk=vacancy.pk - 1)
        except Vacancy.DoesNotExist:
            vacancy_before = None
        try:
            vacancy_after = Vacancy.objects.get(pk=vacancy.pk + 1)
        except Vacancy.DoesNotExist:
            vacancy_after = None
        context['vacancy_before'] = vacancy_before
        context['vacancy_after'] = vacancy_after
        return context


class EventListView(ListView):
    model = Event
    context_object_name = 'event_list'
    template_name = 'e5_app/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MailingForm()
        context['mailing_form'] = form
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
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
                form = VisitorForm(request.POST, event_pk=EventSchedule.objects.get(pk=event_schedule_pk).event.pk)
                if form.is_valid():
                    data = form.cleaned_data
                    Visitor.objects.create(event=data['event'], name=data['name'], mail=data['mail'],
                                           phone=data['phone'], stand=data['stand'])
                    return HttpResponse('''<div class="text-success">
                                                                 Запись принята!</div>''')
                else:
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
        news_list = News.objects.annotate(
            search=SearchVector("name", "description", "created_at", "content"),
        ).filter(search=search_text)
        vacancy_list = Vacancy.objects.annotate(
            search=SearchVector("name", "company__name", "salary", "experience", "schedule", "content"),
        ).filter(search=search_text)
        page_list = HTMLPage.objects.annotate(
            search=SearchVector("content"),
        ).filter(search=search_text)
        works_list = Work.objects.annotate(
            search=SearchVector("name", "description"),
        ).filter(search=search_text)
        if works_list and not page_list.filter(url_name='works'):
            page_list |= HTMLPage.objects.filter(url_name='works')
        employee_list = Employee.objects.annotate(
            search=SearchVector("name", "description"),
        ).filter(search=search_text)
        if employee_list and not page_list.filter(url_name='employees'):
            page_list |= HTMLPage.objects.filter(url_name='employees')
        ctx = {'search_text': search_text, 'news_list': news_list, 'vacancy_list': vacancy_list, 'page_list': page_list}
        return render(request, 'e5_app/search.html', ctx)
    else:
        return redirect('index')
