from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.apps import apps


class ElectricityDetailView(LoginRequiredMixin, View):
    template_name = 'electricity/electricity_detail.html'

    def get(self, request, pk):
        Project = apps.get_model('projects', 'Project')
        p = get_object_or_404(Project, pk=pk, owner=self.request.user)
        ctx = {'project_item': p}
        return render(request=request, context=ctx, template_name=self.template_name)
