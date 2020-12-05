from django.urls import path
from django.views.generic import TemplateView
from .views import ElectricityDetailView

app_name = 'electricity'
urlpatterns = [
    path('', ElectricityDetailView.as_view(), name='detail'),
]