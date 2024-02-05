from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML


class NewsFilterForm(forms.Form):
    start_date = forms.DateField(
        label='От',
        widget=DatePickerInput(options={'format': 'MM/YYYY', })
    )
    end_date = forms.DateField(
        label='До',
        widget=DatePickerInput(options={'format': 'MM/YYYY', })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '/news/filter/'
        self.helper.form_method = 'post'
        self.helper.form_class = 'd-flex flex-column align-items-center text-center'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML("<legend>Выборка</legend>"),
            Field('start_date', css_class='custom-date',),
            Field('end_date', css_class='custom-date',),
            Submit('submit', 'Submit', css_class='btn btn-dark my-1')
        )
