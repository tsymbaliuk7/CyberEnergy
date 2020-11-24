from django import forms
from .models import House
from datetime import date


class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = ['area', 'heat_loss', 'residents', 'water_start_temperature', 'water_end_temperature',
                  'water_shower_temperature', 'shower_number', 'water_bath_temperature', 'bath_number',
                  'q_shower_normal', 'q_bath_normal',
                  'heating_duration', 'heater_power', 'expected_air_temperature',
                  'energy_price',
                  'gaz_price',
                  'coal_price',
                  'wood_price',
                  'pellets_price',
                  'electrical_price',
                  ]
        labels = {'area': 'Площадь дома, м²',
                  'heat_loss': 'Удельные теплопотери здания, Вт/м²',
                  'residents': 'Количество жителей',
                  'water_start_temperature': 'Температура входящей воды, ℃',
                  'water_end_temperature': 'Конечная температура бака, ℃',
                  'water_shower_temperature': 'Температура воды при приеме душа, ℃',
                  'shower_number': 'Количество приемов душа в сутки',
                  'water_bath_temperature': 'Температура воды при приеме ванны, ℃',
                  'bath_number': 'Количество приемов ванны в сутки',
                  'heating_duration': 'Продолжительность нагрева емкости, ч',
                  'heater_power': 'Мощность нагревателя, кВт',
                  'expected_air_temperature': 'Расчетная температура воздуха внутри здания, ℃',
                  'q_shower_normal': 'Объем потребления воды на прием душа, л',
                  'q_bath_normal': 'Объем потребления воды на прием ванны, л',
                  'energy_price': 'Тариф на тепловую энергию, (грн/Гкал)',
                  'gaz_price': 'Цена 1 м³ газа, грн',
                  'coal_price': 'Цена 1 т угля, грн',
                  'wood_price': 'Цена 1 т дров, грн',
                  'pellets_price': 'Цена 1 т пеллет, грн',
                  'electrical_price': 'Тариф на эл. энергию, (грн/кВт⋅час)',
                  }
        widgets = {

            'area': forms.NumberInput(attrs={'step': '0.1', 'min': '1',  'max': '2000'}),
            'heat_loss': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '500'}),
            'residents': forms.NumberInput(attrs={'step': '1', 'min': '1', 'max': '20'}),
            'water_start_temperature': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '100',
                                                                'onchange': "document.getElementById('id_water_end_temperature').min=this.value;"
                                                                            "document.getElementById('id_water_shower_temperature').min=this.value;"
                                                                            "document.getElementById('id_water_bath_temperature').min=this.value;"}),
            'water_end_temperature': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '100',
                                                              'onchange': "document.getElementById('id_water_start_temperature').max=this.value;"
                                                                          "document.getElementById('id_water_shower_temperature').max=this.value;"
                                                                          "document.getElementById('id_water_bath_temperature').max=this.value;"}),
            'water_shower_temperature': forms.NumberInput(attrs={'step': '0.1', 'min': "1", 'max': "100"}),
            'water_bath_temperature': forms.NumberInput(attrs={'step': '0.1', 'min': "1", 'max': "100"}),
            'heating_duration': forms.NumberInput(attrs={'required': True}),
            'heater_power': forms.NumberInput(attrs={'required': False}),
            'shower_number': forms.NumberInput(attrs={'step': '1', 'min': '1', 'max': '10'}),
            'bath_number': forms.NumberInput(attrs={'step': '1', 'min': '1', 'max': '10'}),
            'q_shower_normal': forms.NumberInput(attrs={'step': '1', 'min': '1', 'max': '1000'}),
            'q_bath_normal': forms.NumberInput(attrs={'step': '1', 'min': '1', 'max': '1000'}),
            'energy_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
            'gaz_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
            'coal_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
            'wood_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
            'pellets_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
            'electrical_price': forms.NumberInput(attrs={'step': '0.1', 'min': '1', 'max': '10000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        heating_duration = cleaned_data.get('heating_duration')
        heater_power = cleaned_data.get('heater_power')
        if heater_power is None and heating_duration is None:
            raise forms.ValidationError("Введите либо время нагрева, либо мощность нагревателя.")
