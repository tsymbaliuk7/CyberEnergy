from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.apps import apps
from django.views.generic import DeleteView
from .models import DayOfWeek, ElectricalDevices, UserDevice, SwitchType
from .owner import OwnerDeleteView
from .forms import DeviceForm, UserDeviceForm
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
            swt = get_object_or_404(SwitchType, name='авто')
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
        form = DeviceForm(initial={'project_id': p.id})
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk=None):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = DeviceForm(request.POST, initial={'project_id': p.id})
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
        form = DeviceForm(instance=device, initial={'project_id': p.id})
        ctx = {'form': form, 'project_item': p}
        return render(request, template_name=self.template_name, context=ctx)

    def post(self, request, pk, device_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        device = get_object_or_404(ElectricalDevices, project=p, pk=device_id)
        form = DeviceForm(request.POST, instance=device, initial={'project_id': p.id})
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
        if device.switch_on == hand and device.switch_off == hand:
            form = UserDeviceForm()
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
            pass
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
                                             year=2020, month=3, day=18) - timedelta(hours=float(device.time_of_work)) +
                                    timedelta(hours=round(random.uniform(-0.5, 0.5), 1))).time()
        user_device.device = device
        user_device.save()
        return redirect(reverse('projects:electricity:user_devices', args=[pk]))

