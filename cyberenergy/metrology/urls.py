from django.contrib import admin
from django.urls import path, include
from .views import MetrologyCreateView, MetrologyDeleteView, MetrologyDetailView, MetrologyListView, MetrologyUpdateView

app_name = 'metrology'
urlpatterns = [
    path('', MetrologyListView.as_view(), name='all'),
    path('project/<int:pk>', MetrologyDetailView.as_view(), name='project'),
    path('project/create', MetrologyCreateView.as_view(), name='create'),
    path('project/<int:pk>/delete', MetrologyDeleteView.as_view(), name='delete'),
    path('project/<int:pk>/update', MetrologyUpdateView.as_view(), name='update'),
]
