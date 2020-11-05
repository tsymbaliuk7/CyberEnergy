from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Project
from datetime import date


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'begin_date', 'end_date', 'region']
        labels = {'name': 'Название проекта', 'begin_date': 'Дата начала', 'end_date': 'Дата конца', 'region': 'Регион'}
        widgets = {
            'begin_date': DatePickerInput(format='%d.%m.%Y', attrs={'autocomplete': 'off'}).start_of('event days'),
            'end_date': DatePickerInput(format='%d.%m.%Y', attrs={'autocomplete': 'off'}).end_of('event days'),
        }

    def clean(self):
        cleaned_data = super().clean()
        begin_date = cleaned_data.get("begin_date")
        end_date = cleaned_data.get("end_date")
        if type(date(2012, 1, 1)) == type(end_date) == type(begin_date):
            if end_date < begin_date:
                raise forms.ValidationError("Дата конца должна быть больше даты начала.")
            if begin_date < date(2012, 1, 1) or begin_date >= date(2012, 12, 31) or end_date <= date(2012, 1, 1) \
                    or end_date > date(2012, 12, 31):
                raise forms.ValidationError("Даты должны быть в интервале от 01.01.2012 до 31.12.2012")
