from django.contrib import admin
from django.urls import path, include
from .views import ProjectsListView, ProjectsDetailView, ProjectsCreateView, ProjectsDeleteView, ProjectsUpdateView


app_name = 'projects'
urlpatterns = [
    path('', ProjectsListView.as_view(), name='all'),
    path('<int:pk>', ProjectsDetailView.as_view(), name='project'),
    path('create', ProjectsCreateView.as_view(), name='create'),
    path('<int:pk>/metrology', include('metrology.urls')),
    path('<int:pk>/delete', ProjectsDeleteView.as_view(), name='delete'),
    path('<int:pk>/update', ProjectsUpdateView.as_view(), name='update'),
]
