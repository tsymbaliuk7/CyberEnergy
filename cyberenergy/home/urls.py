from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import MainView

app_name = 'home'
urlpatterns = [
    path('', MainView.as_view(), name='home')
]
