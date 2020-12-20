from django.forms import ModelForm, NumberInput, TextInput
from .models import Windmill, WindmillTower


class WindmillForm(ModelForm):
    class Meta:
        model = Windmill
        exclude = ['project']
        widgets = {
            'price': NumberInput(attrs={'step': '0.5', 'min': '1', 'max': '10000000', 'autocomplete': 'off'}),
            'type': TextInput(attrs={'autocomplete': 'off'})
        }
        labels = {
            'type': 'Название типа ветряка',
            'price': 'Цена(без башни)',
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
            'price': 'Цена(башни), грн',
        }
