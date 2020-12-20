from django.urls import path
from django.views.generic import TemplateView
from .views import WindpowerListView, WindmillCreateView, WindmillUpdateView, WindmillDeleteView, TowerListView, \
    TowerCreateView, TowerUpdateView, TowerDeleteView

app_name = 'windpower'
urlpatterns = [
    path('', WindpowerListView.as_view(), name='detail'),
    path('create', WindmillCreateView.as_view(), name='create'),
    path('update/<int:wind_id>', WindmillUpdateView.as_view(), name='update'),
    path('delete/<int:wind_id>', WindmillDeleteView.as_view(), name='delete'),
    path('<int:wind_id>/towers', TowerListView.as_view(), name='towers_list'),
    path('<int:wind_id>/towers/create', TowerCreateView.as_view(), name='towers_create'),
    path('<int:wind_id>/towers/delete/<int:tower_id>', TowerDeleteView.as_view(), name='towers_delete'),
    path('<int:wind_id>/towers/update/<int:tower_id>', TowerUpdateView.as_view(), name='towers_update'),
]