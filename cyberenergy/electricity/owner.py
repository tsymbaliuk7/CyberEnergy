from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        qs = super(OwnerListView, self).get_queryset()
        return qs.filter(owner=self.request.user).order_by('updated_at')


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
