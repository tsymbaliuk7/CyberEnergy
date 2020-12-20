import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.apps import apps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from .models import DayOfWeek, ElectricalDevices, UserDevice, SwitchType, Tariff, TariffZone, TariffRange, ProjectZone
from .owner import OwnerDeleteView
from .forms import DeviceForm, UserDeviceForm, ZoneForm, RangeForm
import random
from datetime import *

default_devices = [['Микроволновка', 1000], ['Телевизор', 100], ['Холодильник', 200], ['Ноутбук', 50],
                   ['Обогреватель', 1500]]


class ElectricityDevicesView(LoginRequiredMixin, View):
    template_name = 'electricity/electricity_detail.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        electricity_devices = ElectricalDevices.objects.filter(project=pk)
        if not electricity_devices:
            swt = get_object_or_404(SwitchType, name='ручное')
            print(swt)
            for device in default_devices:
                d = ElectricalDevices(name=device[0], power=device[1], switch_on=swt, switch_off=swt, project=p)
                d.save()
            electricity_devices = ElectricalDevices.objects.filter(project=pk)

        ctx = {'project_item': p, 'electricity_devices': electricity_devices}
        return render(request=request, context=ctx, template_name=self.template_name)


class ElectricityDeviceCreateView(LoginRequiredMixin, View):
    template_name = 'electricity/electricity_device_form.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = DeviceForm()
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk=None):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = DeviceForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template_name, ctx)
        device = form.save(commit=False)
        device.project = p
        device.save()
        return redirect(reverse('projects:electricity:detail', args=[pk]))


class ElectricityDeviceUpdateView(LoginRequiredMixin, View):
    template_name = 'electricity/electricity_device_form.html'

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, pk=device_id)
        form = DeviceForm(instance=device)
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, pk=device_id)
        form = DeviceForm(request.POST, instance=device)
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template_name, ctx)
        device = form.save(commit=False)
        device.save()
        return redirect(reverse('projects:electricity:detail', args=[pk]))


class ElectricityDeviceDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, pk=device_id)
        return render(request, template_name='electricity/electricity_user_delete.html', context={'device': device})

    def post(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, pk=device_id)
        ElectricalDevices.objects.filter(pk=device.id).delete()
        return redirect(reverse('projects:electricity:detail', args=[pk]))


class ElectricityUserDevicesView(LoginRequiredMixin, View):
    template_name = 'electricity/electricity_user_devices.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        devices = ElectricalDevices.objects.filter(project=p)
        days = DayOfWeek.objects.all()
        user_devices = UserDevice.objects.filter(device__project=p)
        ctx = {'project': p, 'days': days, 'devices': devices, 'user_devices': user_devices}
        return render(request, self.template_name, ctx)


class ElectricityUserDevicesAddView(LoginRequiredMixin, View):
    template_name = 'electricity/user_device_form.html'

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, id=device_id)
        auto = get_object_or_404(SwitchType, name='авто')
        hand = get_object_or_404(SwitchType, name='ручное')
        form = UserDeviceForm()
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm()
        elif device.switch_on == auto and device.switch_off == auto:
            form.fields.pop('start_time')
            form.fields.pop('end_time')
        elif device.switch_on == hand and device.switch_off == auto:
            form.fields.pop('end_time')
        elif device.switch_on == auto and device.switch_off == hand:
            form.fields.pop('start_time')
        ctx = {'form': form, 'project_item': p, 'device': device}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk, device_id):
        form = UserDeviceForm(request.POST)
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        auto = get_object_or_404(SwitchType, name='авто')
        hand = get_object_or_404(SwitchType, name='ручное')
        device = get_object_or_404(ElectricalDevices, project=p, id=device_id)
        if device.switch_on == auto and device.switch_off == auto:
            form.fields.pop('start_time')
            form.fields.pop('end_time')
        elif device.switch_on == hand and device.switch_off == auto:
            form.fields.pop('end_time')
        elif device.switch_on == auto and device.switch_off == hand:
            form.fields.pop('start_time')
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template_name, ctx)
        user_device = form.save(commit=False)
        start_t = datetime(hour=0, minute=0, year=2020, month=3, day=18)
        end_t = datetime(hour=23, minute=59, year=2020, month=3, day=18)
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm(request.POST)
        elif device.switch_on == auto and device.switch_off == auto:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 8.0), 1)
            start = start_t + timedelta(hours=float(device.time_of_work))
            end = end_t - timedelta(hours=float(device.time_of_work))
            start_rand_hour = random.randint(start.time().hour, end.time().hour)
            start_rand_min = random.randint(0, 59)
            user_device.start_time = time(hour=start_rand_hour, minute=start_rand_min)
            user_device.end_time = (datetime(hour=user_device.start_time.hour, minute=user_device.start_time.minute,
                                             year=2020, month=3, day=18) + timedelta(hours=float(device.time_of_work)) +
                                    timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        elif device.switch_on == hand and device.switch_off == auto:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 5.0), 1)
            user_device.end_time = (datetime(hour=user_device.start_time.hour, minute=user_device.start_time.minute,
                                             year=2020, month=3, day=18) + timedelta(hours=float(device.time_of_work)) +
                                    timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        elif device.switch_on == auto and device.switch_off == hand:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 5.0), 1)
            user_device.start_time = (datetime(hour=user_device.end_time.hour, minute=user_device.end_time.minute,
                                               year=2020, month=3, day=18) - timedelta(
                hours=float(device.time_of_work)) +
                                      timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        user_device.device = device
        user_device.save()
        return redirect(reverse('projects:electricity:user_devices', args=[pk]))


class ElectricityUserDevicesUpdateView(LoginRequiredMixin, View):
    template_name = 'electricity/user_device_form.html'

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        user_device = get_object_or_404(UserDevice, id=device_id)
        device = user_device.device
        auto = get_object_or_404(SwitchType, name='авто')
        hand = get_object_or_404(SwitchType, name='ручное')
        form = UserDeviceForm(instance=user_device)
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm(instance=user_device)
        elif device.switch_on == auto and device.switch_off == auto:
            form.fields.pop('start_time')
            form.fields.pop('end_time')
        elif device.switch_on == hand and device.switch_off == auto:
            form.fields.pop('end_time')
        elif device.switch_on == auto and device.switch_off == hand:
            form.fields.pop('start_time')
        ctx = {'form': form, 'project_item': p, 'device': device}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        auto = get_object_or_404(SwitchType, name='авто')
        hand = get_object_or_404(SwitchType, name='ручное')
        user_device = get_object_or_404(UserDevice, id=device_id)
        device = user_device.device
        form = UserDeviceForm(request.POST, instance=user_device)
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm(request.POST, instance=user_device)
        elif device.switch_on == auto and device.switch_off == auto:
            form.fields.pop('start_time')
            form.fields.pop('end_time')
        elif device.switch_on == hand and device.switch_off == auto:
            form.fields.pop('end_time')
        elif device.switch_on == auto and device.switch_off == hand:
            form.fields.pop('start_time')
        if not form.is_valid():
            ctx = {'form': form, 'project_item': p}
            return render(request, self.template_name, ctx)
        user_device = form.save(commit=False)
        start_t = datetime(hour=0, minute=0, year=2020, month=3, day=18)
        end_t = datetime(hour=23, minute=59, year=2020, month=3, day=18)
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm(request.POST)
        elif device.switch_on == auto and device.switch_off == auto:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 8.0), 1)
            start = start_t + timedelta(hours=float(device.time_of_work))
            end = end_t - timedelta(hours=float(device.time_of_work))
            start_rand_hour = random.randint(start.time().hour, end.time().hour)
            start_rand_min = random.randint(0, 59)
            user_device.start_time = time(hour=start_rand_hour, minute=start_rand_min)
            user_device.end_time = (datetime(hour=user_device.start_time.hour, minute=user_device.start_time.minute,
                                             year=2020, month=3, day=18) + timedelta(hours=float(device.time_of_work)) +
                                    timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        elif device.switch_on == hand and device.switch_off == auto:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 5.0), 1)
            user_device.end_time = (datetime(hour=user_device.start_time.hour, minute=user_device.start_time.minute,
                                             year=2020, month=3, day=18) + timedelta(hours=float(device.time_of_work)) +
                                    timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        elif device.switch_on == auto and device.switch_off == hand:
            if device.time_of_work is None:
                device.time_of_work = round(random.uniform(1.0, 5.0), 1)
            user_device.start_time = (datetime(hour=user_device.end_time.hour, minute=user_device.end_time.minute,
                                               year=2020, month=3, day=18) - timedelta(
                hours=float(device.time_of_work)) +
                                      timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        user_device.save()
        return redirect(reverse('projects:electricity:user_devices', args=[pk]))


class ElectricityUserDevicesDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        user_device = get_object_or_404(UserDevice, id=device_id)
        return render(request, template_name='electricity/user_device_delete.html', context={'device': user_device})

    def post(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        UserDevice.objects.filter(id=device_id).delete()
        return redirect(reverse('projects:electricity:user_devices', args=[pk]))


class ElectricityUserDevicesCloneView(LoginRequiredMixin, View):

    def get(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        user_device = get_object_or_404(UserDevice, id=device_id)
        days = DayOfWeek.objects.all()
        for day in days:
            if not day == user_device.days:
                ud = UserDevice(device=user_device.device, start_time=user_device.start_time, days=day,
                                end_time=user_device.end_time)
                ud.save()
        return redirect(reverse('projects:electricity:user_devices', args=[pk]))


class ElectricityStatisticView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        times = []
        days = DayOfWeek.objects.all()
        for day in days:
            temp = []
            cur_day = datetime(year=2020, month=12, day=10, hour=0, minute=0)
            temp.append(cur_day.time())
            for i in range(240):
                cur_day += timedelta(minutes=10)
                temp.append(cur_day.time())
            times.append(temp)
        devices = ElectricalDevices.objects.filter(project=p)
        devices = [device for device in devices if UserDevice.objects.filter(device__project=p, device=device)]
        device_dict = {}
        for device in devices:
            day_list = []
            for i in range(len(times)):
                temp = []
                ud = UserDevice.objects.filter(device=device, days=days[i])
                for period in times[i]:
                    result = 0
                    for obj in ud:
                        if obj.start_time <= period <= obj.end_time:
                            result += float(obj.device.power)
                    temp.append(result)
                day_list.append(temp)
            day_list = [item for sublist in day_list for item in sublist]
            device_dict[device] = day_list

        first_zone = get_object_or_404(ProjectZone, project=p, zone__name='Единый тариф')
        device_max = {}
        day_list = []
        days = DayOfWeek.objects.all()
        for i in range(len(times)):
            ud = UserDevice.objects.filter(device__project=p, days=days[i])
            temp = []
            for period in times[i]:
                result = 0
                for obj in ud:
                    if obj.start_time <= period <= obj.end_time:
                        result += float(obj.device.power)
                temp.append(result)
            day_list.append(temp)
            device_max[days[i]] = temp

        all_power = [item for sublist in day_list for item in sublist]
        time_times = [item for sublist in times for item in sublist]
        second_zones = ProjectZone.objects.filter(project=p, zone__tariff=2)
        second_zones_result = [[], []]

        for j in range(len(second_zones)):
            second_zones_range = TariffRange.objects.filter(zone=second_zones[j])
            if second_zones_range:
                for rng in second_zones_range:
                    for i in range(len(time_times)):
                        if rng.start_time <= time_times[i] <= rng.end_time:
                            second_zones_result[j].append(all_power[i])
        two_zone = round(((sum(second_zones_result[1]) / 6) / 1000) * float(second_zones[1].price) +
                         ((sum(second_zones_result[0]) / 6) / 1000) * float(second_zones[0].price), 2)
        d = []
        pic = []
        n = []
        third_zones = ProjectZone.objects.filter(project=p, zone__tariff=3)
        third_zones_result = [[], [], []]
        for j in range(len(third_zones)):
            third_zones_ranges = TariffRange.objects.filter(zone=third_zones[j])
            if third_zones_ranges:
                for rng in third_zones_ranges:
                    for i in range(len(time_times)):
                        if rng.start_time <= time_times[i] <= rng.end_time:
                            third_zones_result[j].append(all_power[i])

        three_zone = round(((sum(third_zones_result[2]) / 6) / 1000) * float(third_zones[2].price) +
                           ((sum(third_zones_result[1]) / 6) / 1000) * float(third_zones[1].price) +
                           ((sum(third_zones_result[0]) / 6) / 1000) * float(third_zones[0].price), 2)
        times = [[j.strftime('%H:%M') + ' ' + days[i].name for j in times[i]] for i in range(len(times))]
        times = [item for sublist in times for item in sublist]
        all_power = [item for sublist in day_list for item in sublist]
        for key, value in device_max.items():
            device_max[key] = [sum(value) * (1 / 6), max(value)]
        one_zone = []
        days_list = []
        max_val = []
        for key, value in device_max.items():
            one_zone.append(value[0])
            days_list.append(key.name)
            max_val.append(round(value[1], 1))
        sum_days = one_zone
        total = round(sum(one_zone))
        one_zone = round((sum(one_zone) / 1000) * float(first_zone.price), 2)
        zone_price = [(one_zone / 7) * 30, (two_zone / 7) * 30, (three_zone / 7) * 30]
        zone_price = [round(i, 2) for i in zone_price]
        zone_name = ['Однозонный', 'Двухзонный ', 'Трехзонный ']
        context = {'project': p, 'times': times, 'all_power': all_power, 'device_dict': device_dict,
                   'device_max': device_max, 'zone_price': zone_price, 'zone_name': zone_name, 'days_list': days_list,
                   'sum_days': sum_days, 'max_val': max_val, 'total': total}
        return render(request, 'electricity/electricity_statistic.html', context)


class ElectricityTariffListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        tariffs = Tariff.objects.all()
        zones = TariffZone.objects.all()
        project_zones = ProjectZone.objects.filter(project=pk)
        if not project_zones:
            for zone in zones:
                pz = ProjectZone(zone=zone, project=p, price=0.0)
                pz.save()
        project_zones = ProjectZone.objects.filter(project=pk)
        initial = [pz.price for pz in project_zones]
        name = [field.name for field in ZoneForm()]
        initial = dict(zip(name, initial))
        form = ZoneForm(initial=initial)
        ranges = TariffRange.objects.filter(zone__project=p)
        ctx = {'project': p, 'tariffs': tariffs, 'zones': zones, 'project_zones': project_zones, 'form': form,
               'ranges': ranges}
        return render(request, 'electricity/electricity_tariff.html', ctx)

    def post(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        tariffs = Tariff.objects.all()
        zones = TariffZone.objects.all()
        project_zones = ProjectZone.objects.filter(project=pk)
        form = ZoneForm(request.POST)
        if not form.is_valid():
            ctx = {'project': p, 'tariffs': tariffs, 'zones': zones, 'project_zones': project_zones, 'form': form}
            return render(request, 'electricity/electricity_tariff.html', ctx)
        for pz in project_zones:
            pz.price = form.cleaned_data['field{}'.format(pz.zone.id)]
            pz.save()
        return redirect(reverse('projects:electricity:tariffs', args=[pk]) + '#tariff_form')


class ElectricityTariffAddView(LoginRequiredMixin, View):
    def get(self, request, pk, tariff_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        tariff_zones = ProjectZone.objects.filter(project=p, zone__tariff_id=tariff_id)
        form = RangeForm()
        form.fields['zone'].queryset = tariff_zones
        ctx = {'form': form, 'project': p}
        return render(request, 'electricity/electricity_tariff_form.html', ctx)

    def post(self, request, pk, tariff_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = RangeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'project': p}
            return render(request, 'electricity/electricity_tariff_form.html', ctx)
        tariff_range = form.save(commit=False)
        tariff_range.save()
        return redirect(reverse('projects:electricity:tariffs', args=[pk]) + '#tariff-ranges')


class ElectricityTariffUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, tariff_id, range_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        tariff_zones = ProjectZone.objects.filter(project=p, zone__tariff_id=tariff_id)
        tariff_range = get_object_or_404(TariffRange, pk=range_id)
        form = RangeForm(instance=tariff_range)
        form.fields['zone'].queryset = tariff_zones
        ctx = {'form': form, 'project': p}
        return render(request, 'electricity/electricity_tariff_form.html', ctx)

    def post(self, request, pk, tariff_id, range_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        tariff_range = get_object_or_404(TariffRange, pk=range_id)
        form = RangeForm(request.POST, instance=tariff_range)
        if not form.is_valid():
            ctx = {'form': form, 'project': p}
            return render(request, 'electricity/electricity_tariff_form.html', ctx)
        tariff_range = form.save(commit=False)
        tariff_range.save()
        return redirect(reverse('projects:electricity:tariffs', args=[pk]) + '#tariff-ranges')


class ElectricityTariffDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, range_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        user_device = get_object_or_404(TariffRange, id=range_id)
        return render(request, template_name='electricity/tariff_range_delete.html',
                      context={'device': user_device, 'project': p})

    def post(self, request, pk, range_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        TariffRange.objects.filter(id=range_id).delete()
        return redirect(reverse('projects:electricity:tariffs', args=[pk]) + '#tariff-ranges')
