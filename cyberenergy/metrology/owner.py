from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        qs = super(OwnerListView, self).get_queryset()
        return qs.filter(owner=self.request.user).order_by('updated_at')


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super(OwnerUpdateView, self).get_object()
        obj.set_is_changed(True)
        return obj



class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
