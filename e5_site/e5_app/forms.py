from bootstrap_datepicker_plus.widgets import MonthPickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from crispy_forms.bootstrap import PrependedText
from django.urls import reverse
from datetime import datetime


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
        self.helper.layout = Layout(PrependedText('mail', 'Почта', placeholder="example@mail.ru"))
        self.helper.add_input(Submit('submit_mailing', 'Оформить подписку', css_class='btn btn-warning', ))
