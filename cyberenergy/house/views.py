from io import BytesIO
import urllib.request

import pdfkit
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views import View
from xhtml2pdf import pisa
from selenium import webdriver

from .models import House
from .forms import HouseForm
from .exel_reader import exel_reader

import numpy as np
from decimal import Decimal


class HouseDetailView(View):
    template = 'house/house_detail.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        MetrologyData = apps.get_model('metrology', 'MetrologyData')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        house = House.objects.filter(project=p)
        if not house:
            return redirect(reverse('projects:house:create', kwargs={'pk': pk}))
        house_item = get_object_or_404(House, project=p)
        if MetrologyData.objects.filter(metrology=p).count() == 0 or p.is_changed:
            MetrologyData.objects.filter(metrology=p).delete()
            exel_reader(p)
            p.set_is_changed(False)
            p.save()
        Q = float(Decimal(house_item.area) * (Decimal(house_item.heat_loss) / 1000))
        k = round(Q/(float(-house_item.expected_air_temperature + p.region.temperature)), 4)
        b = round((-Q * float(house_item.expected_air_temperature)) / (float(-house_item.expected_air_temperature + p.region.temperature)), 4)
        step = Q / 20
        q_range = [round(i, 3) for i in np.arange(Q, 0, -step)]
        q_range.append(0)
        temperature_range = [(q - b)/k for q in q_range]
        temperature_range = [round(i, 1) for i in temperature_range]
        md = MetrologyData.objects.filter(metrology=p).order_by('date')
        temperature_list = list(set([int(data.temperature) for data in md]))
        temperature_list.sort()
        temperature_hours = []
        for i in temperature_list:
            temperature_hours.append(md.filter(temperature=i).count() / 2)
        q_list = [k*t + b for t in temperature_list]
        energy_loss = round(sum([q_list[i] * temperature_hours[i] for i in range(len(temperature_list))]), 3)

        project_days = p.end_date - p.begin_date
        W = float(house_item.energy) * project_days.days + energy_loss
        heat_boiler = W * float(house_item.energy_price) * 0.000116222
        gaz_boiler = W * 0.1 * float(house_item.gaz_price) * 0.534
        coal_boiler = W * 0.00025 * float(house_item.coal_price)
        wood_boiler = W * 0.0004 * float(house_item.wood_price)
        pellet_boiler = W * 0.0002 * float(house_item.pellets_price)
        electr_boiler = W * float(house_item.electrical_price)
        boiler_price = [heat_boiler, gaz_boiler, coal_boiler, wood_boiler, pellet_boiler, electr_boiler]
        boiler_price = [round(i, 2) for i in boiler_price]
        boiler_name = ['Тепловой', 'Газовый', 'Угольный', 'Древесный', 'Пеллетный', 'Электрический']
        price = list(map(lambda x: x*1.03, [8034, 8501, 5560, 6200, 6350, 5000]))
        ctx = {'project_item': p, 'house': house, 'house_item': house_item, 'temperature_range': temperature_range,
               'q_range': q_range, 'energy_loss': energy_loss, 'k': k, 'b': b, 'boiler_price': boiler_price,
               'boiler_name': boiler_name, 'price': price}
        return render(request, template_name=self.template, context=ctx)


class HouseCreateView(View):
    model = House
    template = 'house/house_form.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = HouseForm()
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template, context=ctx)

    def post(self, request, pk=None):
        form = HouseForm(request.POST)
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        rad = request.POST['heating']
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template, ctx)
        house = form.save(commit=False)
        house.q_bath = house.bath_number * house.q_bath_normal
        house.q_shower = house.shower_number * house.q_shower_normal
        house.shower_water_volume = house.q_shower * ((house.water_shower_temperature -
                                                       house.water_start_temperature) / (
                                                              house.water_end_temperature - house.water_start_temperature))
        house.bath_water_volume = house.q_bath * ((house.water_bath_temperature -
                                                   house.water_start_temperature) / (
                                                          house.water_end_temperature - house.water_start_temperature))
        house.total_water_volume = (house.shower_water_volume + house.bath_water_volume) / Decimal(998.23)
        house.energy = Decimal(1.163) * house.total_water_volume * (
                house.water_end_temperature - house.water_start_temperature)
        if rad == 'duration':
            house.heater_power = house.energy / house.heating_duration
        elif rad == 'power':
            house.heating_duration = house.energy / house.heater_power
        house.project = p
        house.save()
        return redirect(reverse('projects:house:detail', args=[pk]))


class HouseUpdateView(View):
    model = House
    template = 'house/house_form.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        house = House.objects.filter(project=p)
        if not house:
            return redirect(reverse('projects:house:create', kwargs={'pk': pk}))
        house = get_object_or_404(House, project=p)
        form = HouseForm(instance=house)
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template, context=ctx)

    def post(self, request, pk=None):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        house = get_object_or_404(House, project=p)
        form = HouseForm(request.POST, instance=house)
        rad = request.POST['heating']
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template, ctx)
        house = form.save(commit=False)
        house.q_bath = house.bath_number * house.q_bath_normal
        house.q_shower = house.shower_number * house.q_shower_normal
        house.shower_water_volume = house.q_shower * ((house.water_shower_temperature -
                                                                   house.water_start_temperature) / (
                                                                              house.water_end_temperature - house.water_start_temperature))
        house.bath_water_volume = house.q_bath * ((house.water_bath_temperature -
                                                                house.water_start_temperature) / (
                                                                           house.water_end_temperature - house.water_start_temperature))
        house.total_water_volume = (house.shower_water_volume + house.bath_water_volume) / Decimal(998.23)
        house.energy = Decimal(1.163) * house.total_water_volume * (
                house.water_end_temperature - house.water_start_temperature)
        if rad == 'duration':
            house.heater_power = house.energy / house.heating_duration
        elif rad == 'power':
            house.heating_duration = house.energy / house.heater_power
        house.save()
        return redirect(reverse('projects:house:detail', kwargs={'pk': pk}))