from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .models import Project
from .owner import OwnerListView, OwnerDeleteView
from .forms import ProjectForm


class ProjectsListView(OwnerListView):
    model = Project


class ProjectsDetailView(LoginRequiredMixin, View):
    template = 'projects/project_detail.html'

    def get(self, request, pk):
        obj = get_object_or_404(Project, pk=pk, owner=self.request.user)
        context = {'project_detail': obj}
        return render(request, template_name=self.template, context=context)


class ProjectsCreateView(LoginRequiredMixin, View):
    model = Project
    template = 'projects/project_form.html'

    def get(self, request):
        form = ProjectForm()
        ctx = {'form': form}
        return render(request, template_name=self.template, context=ctx)

    def post(self, request):
        form = ProjectForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        prj = form.save(commit=False)
        prj.owner = self.request.user
        prj.save()
        return redirect(prj.get_absolute_url())


class ProjectsUpdateView(View):
    model = Project
    template = 'projects/project_form.html'

    def get(self, request, pk):
        mtr = get_object_or_404(Project, id=pk, owner=self.request.user)
        form = ProjectForm(instance=mtr)
        ctx = {'form': form}
        return render(request, template_name=self.template, context=ctx)

    def post(self, request, pk=None):
        mtr = get_object_or_404(Project, id=pk, owner=self.request.user)
        form = ProjectForm(request.POST, instance=mtr)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        mtr = form.save(commit=False)
        mtr.set_is_changed(True)
        mtr.save()
        return redirect(mtr.get_absolute_url())


class ProjectsDeleteView(OwnerDeleteView):
    model = Project
    success_url = reverse_lazy('projects:all')
