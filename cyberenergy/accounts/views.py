from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = '/accounts/login?next=/'
    template_name = 'accounts/signup.html'
