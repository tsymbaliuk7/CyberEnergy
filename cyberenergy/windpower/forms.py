from django import forms
from django.forms import ModelForm, NumberInput, TextInput
from .models import Windmill, WindmillTower


class WindmillForm(ModelForm):
    class Meta:
        model = Windmill
        exclude = ['project']
        widgets = {
            'price': NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '10000000', 'autocomplete': 'off'}),
            'name': TextInput(attrs={'autocomplete': 'off'})
        }
        labels = {
            'name': 'Название ветряка',
            'price': 'Цена(без башни), евро',
            'type': 'Тип ветряка'
        }


class TowerForm(ModelForm):
    class Meta:
        model = WindmillTower
        exclude = ['windmill']
        widgets = {
            'price': NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '10000000', 'autocomplete': 'off'}),
            'height': NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '10000000', 'autocomplete': 'off'})
        }
        labels = {
            'height': 'Высота ветряка, м',
            'price': 'Цена(башни), евро',
        }


class MaxCharForm(forms.Form):
    value = forms.DecimalField(label='Измените максимальную мощность, кВт:',
                               widget=forms.NumberInput(attrs={'step': '0.05', 'min': '0.05', 'max': '1000000'}))
