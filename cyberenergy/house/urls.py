from django.urls import path
from .views import HouseDetailView, HouseUpdateView, HouseCreateView


app_name = 'house'
urlpatterns = [
    path('', HouseDetailView.as_view(), name='detail'),
    path('create', HouseCreateView.as_view(), name='create'),
    path('update', HouseUpdateView.as_view(), name='update'),
]