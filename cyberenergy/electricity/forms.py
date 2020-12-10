from django.forms import ModelForm
from django import forms
from .models import ElectricalDevices, UserDevice
from bootstrap_datepicker_plus import TimePickerInput


class DeviceForm(forms.ModelForm):
    class Meta:
        model = ElectricalDevices
        fields = ['name', 'power', 'switch_on', 'switch_off', 'time_of_work']
        labels = {'name': 'Название прибора',
                  'power': 'Мощность, Вт',
                  'switch_on': 'Режим включения',
                  'switch_off': 'Режим выключения',
                  'time_of_work': 'Среднее время работы, ч'}
        widgets = {'time_of_work': forms.NumberInput(attrs={'required': True, 'step': '0.1', 'min': '0.1', 'max': '10'}),
                   'power': forms.NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '100000'})}





class UserDeviceForm(forms.ModelForm):
    class Meta:
        model = UserDevice
        fields = '__all__'
        exclude = ['device']
        widgets = {
            'start_time': TimePickerInput(attrs={'autocomplete': 'off'}).start_of('event day'),
            'end_time': TimePickerInput(attrs={'autocomplete': 'off'}).end_of('event day'),
        }