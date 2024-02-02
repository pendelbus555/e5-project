from bootstrap_datepicker_plus.widgets import YearPickerInput, MonthPickerInput, DatePickerInput
from django import forms


class NewsFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(options={'format': 'MM/YYYY', })
    )
    end_date = forms.DateField(
        widget=DatePickerInput(options={'format': 'MM/YYYY', })
    )
    # start_year = forms.DateField(widget=YearPickerInput())
    # start_mont = forms.DateField(widget=MonthPickerInput(range_from=start_year))
    # end_year = forms.DateField(widget=YearPickerInput())
    # end_month = forms.DateField(widget=MonthPickerInput(range_from=end_year))
