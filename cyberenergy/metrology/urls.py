from django.contrib import admin
from django.urls import path, include
from .views import MetrologyDetailView

app_name = 'metrology'
urlpatterns = [
    path('', MetrologyDetailView.as_view(), name='project'),
]
