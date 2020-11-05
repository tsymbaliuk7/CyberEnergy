from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import MetrologyData, WindDirection, SolarData
from django.contrib.auth.mixins import LoginRequiredMixin
from .exel_reader import exel_reader
from django.db.models import Q
from django.apps import apps


class MetrologyDetailView(LoginRequiredMixin, View):
    template_name = 'metrology/metrology_detail.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        m = get_object_or_404(Project, pk=pk, owner=self.request.user)
        if MetrologyData.objects.filter(metrology=m).count() == 0 or m.is_changed:
            MetrologyData.objects.filter(metrology=m).delete()
            exel_reader(m)
            m.set_is_changed(False)
            m.save()
        md = MetrologyData.objects.filter(metrology=m).order_by('date')
        sd = SolarData.objects.filter(metrology=m).order_by('date')

        date_list = []
        temperature_for_date = []
        for elem in md:
            date_list.append(elem.date.strftime('%d.%m.%Y %H:%M'))
            temperature_for_date.append(int(elem.temperature))

        solar_date = []
        solar_for_date = []
        temp = list(range(8, 18))
        for elem in sd:
            if elem.date.hour in temp:
                solar_date.append(elem.date.strftime('%d.%m %H:%M'))
                solar_for_date.append(int(elem.value))

        solar_list = list(set([int(data.value) for data in sd]))
        solar_list.sort()
        solar_hours = []
        for i in solar_list:
            solar_hours.append(sd.filter(value=i).count())

        wind_list = list(set([int(data.wind_speed) for data in md]))
        wind_list.sort()
        wind_hours = []
        for i in wind_list:
            wind_hours.append(md.filter(wind_speed=i).count() / 2)

        temperature_list = list(set([int(data.temperature) for data in md]))
        temperature_list.sort()
        temperature_hours = []
        for i in temperature_list:
            temperature_hours.append(md.filter(temperature=i).count() / 2)

        wind_dir = ['Северный', 'С-В', 'Восточный', 'Ю-В', 'Южный', 'Ю-З', 'Западный', 'С-З']
        wind_speed = ['1-2 м/c', '2-5 м/c', '5-7 м/c', '7-9 м/c', '>9 м/c']
        without_calm = md.filter(wind_speed__gt=0)
        without_calm = without_calm.filter(~Q(wind_direction=WindDirection.objects.get(name="Переменный")))
        wind_speed_count = [without_calm.filter(wind_speed__gte=1, wind_speed__lt=2),
                            without_calm.filter(wind_speed__gte=2, wind_speed__lt=5),
                            without_calm.filter(wind_speed__gte=5, wind_speed__lt=7),
                            without_calm.filter(wind_speed__gte=7, wind_speed__lt=9),
                            without_calm.filter(wind_speed__gte=9)]
        wind_speed_data = [[[dir_name, round(
            i.filter(wind_direction=WindDirection.objects.get(name=dir_name)).count() / without_calm.count() * 100, 1)]
                            for dir_name in wind_dir] for i in wind_speed_count]
        wind_speed = [
            '{} ({} %)'.format(wind_speed[i], round(wind_speed_count[i].count() / without_calm.count() * 100), 1) for i
            in range(len(wind_speed))]
        wind_rose_data = dict(zip(wind_speed, wind_speed_data))
        calm_percent = '{} ({} %)'.format('Штиль', round((md.filter(wind_speed=0).count() / md.count()) * 100, 1))
        change_percent = '{} ({} %)'.format('Переменный', round(
            (md.filter(wind_direction=WindDirection.objects.get(name="Переменный")).count() / md.count()) * 100, 1))

        context = {'metrology_list': m, 'temperature_list': temperature_list, 'temperature_hours': temperature_hours,
                   'wind_list': wind_list,
                   'wind_hours': wind_hours, 'date_list': date_list, 'temperature_for_date': temperature_for_date,
                   'calm_percent': calm_percent,
                   'wind_rose_data': wind_rose_data, 'solar_list': solar_list, 'solar_hours': solar_hours,
                   'solar_date': solar_date,
                   'solar_for_date': solar_for_date, 'change_percent': change_percent}
        return render(request, template_name=self.template_name, context=context)
