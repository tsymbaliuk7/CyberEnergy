from django.forms import ModelForm
from django import forms
from .models import ElectricalDevices, UserDevice, ProjectZone, TariffRange
from bootstrap_datepicker_plus import TimePickerInput


class DeviceForm(forms.ModelForm):
    class Meta:
        model = ElectricalDevices
        fields = ['name', 'power', 'switch_on', 'switch_off', 'time_of_work']
        labels = {'name': 'Название прибора',
                  'power': 'Мощность, Вт',
                  'switch_on': 'Режим включения',
                  'switch_off': 'Режим выключения',
                  'time_of_work': 'Среднее время работы (необязательно), ч'}
        widgets = {
            'time_of_work': forms.NumberInput(attrs={'required': True, 'step': '0.1', 'min': '0.1', 'max': '10'}),
            'power': forms.NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '100000'})}


class UserDeviceForm(forms.ModelForm):
    class Meta:
        model = UserDevice
        fields = '__all__'
        exclude = ['device']
        labels = {'days': 'День',
                  'end_time': 'Время выключения',
                  'start_time': 'Время включения', }
        widgets = {
            'start_time': TimePickerInput(attrs={'autocomplete': 'off'}).start_of('event day'),
            'end_time': TimePickerInput(attrs={'autocomplete': 'off'}).end_of('event day'),
        }


class ZoneForm(forms.Form):
    field1 = forms.DecimalField(label='1', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))
    field2 = forms.DecimalField(label='2', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))
    field3 = forms.DecimalField(label='3', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))
    field4 = forms.DecimalField(label='4', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))
    field5 = forms.DecimalField(label='5', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))
    field6 = forms.DecimalField(label='6', widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000'}))


class RangeForm(forms.ModelForm):
    class Meta:
        model = TariffRange
        fields = '__all__'
        labels = {
            'start_time': 'Начало',
            'end_time': 'Конец',
            'zone': 'Тарифная зона'
        }
        widgets = {
            'start_time': TimePickerInput(attrs={'autocomplete': 'off'}).start_of('event day'),
            'end_time': TimePickerInput(attrs={'autocomplete': 'off'}).end_of('event day'),
        }