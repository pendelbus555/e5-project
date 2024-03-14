from bootstrap_datepicker_plus.widgets import MonthPickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, Div
from crispy_forms.bootstrap import PrependedText, InlineRadios
from django.urls import reverse
from .models import EventSchedule
from datetime import datetime
from phonenumber_field.formfields import PhoneNumberField


class NewsFilterForm(forms.Form):
    start_date = forms.DateField(
        label='From',
        input_formats=['%Y-%m-%d', '%Y-%m', ],
    )
    end_date = forms.DateField(
        label='To',
        input_formats=['%Y-%m-%d', '%Y-%m', ],
    )

    def __init__(self, *args, **kwargs):
        min_date = kwargs.pop('min_date', None)
        max_date = kwargs.pop('max_date', None)
        super().__init__(*args, **kwargs)
        if min_date and max_date:
            self.fields['start_date'].widget = MonthPickerInput(
                options={'format': 'YYYY-MM', 'minDate': min_date,
                         'maxDate': max_date, })
            self.fields['start_date'].initial = min_date

            self.fields['end_date'].widget = MonthPickerInput(
                options={'format': 'YYYY-MM', 'minDate': min_date,
                         'maxDate': max_date, })
            self.fields['end_date'].initial = max_date

        self.helper = FormHelper()
        self.helper.form_action = reverse('news_filter')
        self.helper.form_method = 'post'
        self.helper.form_class = 'd-flex flex-column align-items-center text-center'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML("<legend>Выборка</legend>"),
            Field('start_date', css_class='custom-date', ),
            Field('end_date', css_class='custom-date', ),
            Submit('submit', 'Submit', css_class='btn btn-dark my-1')
        )


class MailingForm(forms.Form):
    mail = forms.EmailField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = 'post'
        self.helper.form_action = 'events'
        self.helper.attrs = {'hx_boost': 'true', 'hx-target': 'this'}
        self.helper.layout = Layout(PrependedText('mail', 'Почта', placeholder="example@example.ru"))
        self.helper.add_input(Submit('submit_mailing', 'Оформить подписку', css_class='btn btn-warning', ))


class VisitorForm(forms.Form):
    STAND_CHOICES = [
        ('ab', 'Абитуриент'),
        ('11', '11 класс'),
        ('10', '10 класс'),
        ('dr', 'Другое'),
    ]
    event = forms.ModelChoiceField(empty_label=None, queryset=EventSchedule.objects.none())
    name = forms.CharField(max_length=100, )
    mail = forms.EmailField()
    phone = PhoneNumberField(region='RU')
    stand = forms.ChoiceField(widget=forms.RadioSelect, choices=STAND_CHOICES, label='')

    def __init__(self, *args, **kwargs):
        event_pk = kwargs.pop('event_pk', None)
        super().__init__(*args, **kwargs)
        event_schedule = EventSchedule.objects.filter(event__pk=event_pk)
        self.fields['event'].queryset = event_schedule
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_method = 'post'
        self.helper.form_action = 'events'
        self.helper.attrs = {'hx_boost': 'true', 'hx-target': 'this'}
        self.helper.layout = Layout(
            HTML(f"<p class='text-center'>{event_schedule[0].event.date} {event_schedule[0].event.name}</p>"),
            PrependedText('event', 'Время'),
            PrependedText('name', 'ФИО', placeholder="Иванов Иван Иванович"),
            PrependedText('mail', 'Почта', placeholder="example@mail.ru"),
            PrependedText('phone', 'Телефон'),
            InlineRadios('stand'),
            Submit('submit_visitor', 'Отправить', css_class='btn btn-primary'),
            Div(css_id='visitor_errors',css_class='text-danger'),
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split(' ')) != 3:
            raise forms.ValidationError('Введите правильное ФИО (3 слова через пробел)')
        return name
