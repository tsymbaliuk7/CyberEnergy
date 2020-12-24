import random

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Windmill, WindmillTower, WindmillCharacteristics, WindmillType
from .exel_reader import exel_reader, fill_wind_characteristics
from .forms import WindmillForm, TowerForm, MaxCharForm
from django.db.models import Max


default_max_values = [350, 1000, 600, 2000, 444]
default_windmill = [[15000, [[8000, 80], [5000, 50], [10000, 100]], 1],
                    [99999, [[5555, 90], [4334, 67]], 2],
                    [87777, [[2112, 40]], 1],
                    [30000, [[7000, 30], [5000, 63]], 2],
                    [12000, [[8000, 80], [66450, 125], [13344, 92]], 1]]


class WindpowerListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        # MetrologyData = apps.get_model('metrology', 'MetrologyData')
        # if MetrologyData.objects.filter(metrology=p).count() == 0 or p.is_changed:
        #     MetrologyData.objects.filter(metrology=p).delete()
        #     exel_reader(p)
        #     p.set_is_changed(False)
        #     p.save()
        #
        windmills = Windmill.objects.filter(project=p)
        if not windmills:
            for i in range(len(default_windmill)):
                wm = Windmill(name='Windmill{}'.format(i), price=default_windmill[i][0], project=p,
                              type=get_object_or_404(WindmillType, pk=default_windmill[i][2]))
                wm.save()
                dict_characteristics = fill_wind_characteristics(default_max_values[i])
                for key, value in dict_characteristics.items():
                    wc = WindmillCharacteristics(windspeed=key, power=value, windmill=wm)
                    wc.save()
                for elem in default_windmill[i][1]:
                    wmt = WindmillTower(windmill=wm, price=elem[0], height=elem[1])
                    wmt.save()
            windmills = Windmill.objects.filter(project=p)
        ctx = {'windmills': windmills, 'project': p}
        return render(request, 'windpower/windpower_detail.html', ctx)


class WindmillCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = WindmillForm()
        ctx = {'form': form, 'project': p}
        return render(request, 'windpower/windpower_form.html', ctx)

    def post(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        form = WindmillForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'project': p}
            return render(request, 'windpower/windpower_form.html', ctx)
        windmill = form.save(commit=False)
        windmill.project = p
        windmill.save()
        return redirect(reverse('projects:windpower:detail', args=[pk]))


class WindmillUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        windmill = get_object_or_404(Windmill, project=p, id=wind_id)
        form = WindmillForm(instance=windmill)
        ctx = {'form': form, 'project': p}
        return render(request, 'windpower/windpower_form.html', ctx)

    def post(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        windmill = get_object_or_404(Windmill, project=p, id=wind_id)
        form = WindmillForm(request.POST, instance=windmill)
        if not form.is_valid():
            ctx = {'form': form, 'project': p}
            return render(request, 'windpower/windpower_form.html', ctx)
        windmill = form.save(commit=False)
        windmill.save()
        return redirect(reverse('projects:windpower:detail', args=[pk]))


class WindmillDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        windmill = get_object_or_404(Windmill, project=p, id=wind_id)
        ctx = {'project': p, 'windmill': windmill}
        return render(request, 'windpower/windmill_delete.html', ctx)

    def post(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        Windmill.objects.filter(project=p, id=wind_id).delete()
        return redirect(reverse('projects:windpower:detail', args=[pk]))


class TowerListView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        windmill_towers = WindmillTower.objects.filter(windmill=wind_id)
        wc = WindmillCharacteristics.objects.filter(windmill=wind)
        if not wc:
            dict_characteristics = fill_wind_characteristics(random.choice(default_max_values))
            for key, value in dict_characteristics.items():
                wc = WindmillCharacteristics(windspeed=key, power=value, windmill=wind)
                wc.save()
            wc = WindmillCharacteristics.objects.filter(windmill=wind)
        max_value = float(wc.aggregate(Max('power'))['power__max'])
        form = MaxCharForm(initial={'value': max_value})
        power = [float(i.power) for i in wc]
        windspeed = [i.windspeed for i in wc]
        ctx = {'towers': windmill_towers, 'project': p, 'windmill': wind, 'wind_characteristics': wc, 'form': form,
               'windspeed': windspeed, 'power': power}
        return render(request, 'windpower/windtower_detail.html', ctx)

    def post(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        form = MaxCharForm(request.POST)
        windmill_towers = WindmillTower.objects.filter(windmill=wind_id)
        wc = WindmillCharacteristics.objects.filter(windmill=wind)
        power = [float(i.power) for i in wc]
        windspeed = [i.windspeed for i in wc]
        if not form.is_valid():
            ctx = {'towers': windmill_towers, 'project': p, 'windmill': wind, 'wind_characteristics': wc, 'form': form,
                   'windspeed': windspeed, 'power': power}
            return render(request, 'windpower/windtower_detail.html', ctx)
        WindmillCharacteristics.objects.filter(windmill=wind).delete()
        max_value = float(form.cleaned_data['value'])
        dict_characteristics = fill_wind_characteristics(max_value)
        for key, value in dict_characteristics.items():
            wc = WindmillCharacteristics(windspeed=key, power=value, windmill=wind)
            wc.save()
        return redirect(reverse('projects:windpower:towers_list', args=[pk, wind_id]) + '#wind_characteristics_header')


class TowerCreateView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        form = TowerForm()
        ctx = {'form': form, 'project': p, 'windmill': wind}
        return render(request, 'windpower/tower_form.html', ctx)

    def post(self, request, pk, wind_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        form = TowerForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'project': p, 'windmill': wind}
            return render(request, 'windpower/tower_form.html', ctx)
        tower = form.save(commit=False)
        tower.windmill = wind
        tower.save()
        return redirect(reverse('projects:windpower:towers_list', args=[pk, wind_id]))


class TowerUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id, tower_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        tower = get_object_or_404(WindmillTower, id=tower_id, windmill=wind)
        form = TowerForm(instance=tower)
        ctx = {'form': form, 'project': p, 'windmill': wind}
        return render(request, 'windpower/tower_form.html', ctx)

    def post(self, request, pk, wind_id, tower_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        tower = get_object_or_404(WindmillTower, id=tower_id, windmill=wind)
        form = TowerForm(request.POST, instance=tower)
        if not form.is_valid():
            ctx = {'form': form, 'project': p, 'windmill': wind}
            return render(request, 'windpower/tower_form.html', ctx)
        tower = form.save(commit=False)
        tower.save()
        return redirect(reverse('projects:windpower:towers_list', args=[pk, wind_id]))


class TowerDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, wind_id, tower_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        windmill = get_object_or_404(Windmill, project=p, id=wind_id)
        tower = get_object_or_404(WindmillTower, id=tower_id, windmill=windmill)
        ctx = {'project': p, 'tower': tower}
        return render(request, 'windpower/tower_delete.html', ctx)

    def post(self, request, pk, wind_id, tower_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        WindmillTower.objects.filter(id=tower_id, windmill=wind_id, windmill__project=p).delete()
        return redirect(reverse('projects:windpower:towers_list', args=[pk, wind_id]))


class WindmillInfoView(View):
    def get(self, request, pk, wind_id, tower_id):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        MetrologyData = apps.get_model('metrology', 'MetrologyData')
        if MetrologyData.objects.filter(metrology=p).count() == 0 or p.is_changed:
            MetrologyData.objects.filter(metrology=p).delete()
            exel_reader(p)
            p.set_is_changed(False)
            p.save()
        metrology_data = MetrologyData.objects.filter(metrology=p)
        wind = get_object_or_404(Windmill, id=wind_id, project=p)
        tower = get_object_or_404(WindmillTower, id=tower_id, windmill=wind)
        wind_range = list(filter(lambda x: x > 0, set([i.wind_speed for i in metrology_data])))
        wind_fixed = [int(i * ((float(tower.height)/10) ** 0.14)) for i in wind_range]
        wind_count = [MetrologyData.objects.filter(metrology=p, wind_speed=i).count()/2 for i in wind_range]
        power_result = list(map(lambda x, y: x*y, wind_fixed, wind_count))
        total_power = sum(power_result)
        co2 = (total_power/1000) * 0.94
        income = total_power * 0.164
        co2_income = co2 * 10
        time_to_clean_income = ((float(tower.price) + float(wind.price))/(income + co2_income))*(p.end_date - p.begin_date).days
        ctx = {'project': p, 'power': power_result, 'wind_fixed': wind_fixed, 'total_power': total_power, 'co2': co2,
               'income': income, 'co2_income': co2_income, 'time_to_clean_income': time_to_clean_income}
        return render(request, 'windpower/windpower_info.html', ctx)
