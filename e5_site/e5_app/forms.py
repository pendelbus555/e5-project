from bootstrap_datepicker_plus.widgets import DatePickerInput, MonthPickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from django.urls import reverse


class NewsFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        minDate = kwargs.pop('minDate', None)
        maxDate = kwargs.pop('maxDate', None)
        super().__init__(*args, **kwargs)

        self.fields['start_date'] = forms.DateField(
            label='From',
            input_formats=['%Y-%m-%d', '%Y-%m', ],
            widget=MonthPickerInput( options={'format':'YYYY-MM','minDate': minDate, 'maxDate': maxDate, 'useStrict':True}),
        )

        self.fields['end_date'] = forms.DateField(
            label='To',
            widget=MonthPickerInput( options={'format':'YYYY-MM','minDate': minDate, 'maxDate': maxDate, }),
            input_formats=['%Y-%m-%d', '%Y-%m', ],
        )

        self.helper = FormHelper()
        #self.helper.form_action = reverse('news_filter')
        self.helper.form_method = 'post'
        self.helper.form_class = 'd-flex flex-column align-items-center text-center'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML("<legend>Выборка</legend>"),
            Field('start_date', css_class='custom-date', ),
            Field('end_date', css_class='custom-date', ),
            Submit('submit', 'Submit', css_class='btn btn-dark my-1')
        )
