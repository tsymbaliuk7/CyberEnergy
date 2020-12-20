from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Windmill, WindmillTower, WindmillCharacteristics
from .exel_reader import exel_reader
from .forms import WindmillForm, TowerForm

default_windmill = [[150000, [[80000, 80], [50000, 50], [100000, 100]]],
                    [999999, [[55555, 90], [43234, 67]]],
                    [877777, [[21312, 40]]],
                    [300000, [[70000, 30], [50000, 63]]],
                    [120000, [[80000, 80], [665450, 125], [123344, 92]]]]


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
                wm = Windmill(type='Windmill{}'.format(i), price=default_windmill[i][0], project=p)
                wm.save()
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
        ctx = {'towers': windmill_towers, 'project': p, 'windmill': wind}
        return render(request, 'windpower/windtower_detail.html', ctx)


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
