from django.urls import path
from django.views.generic import TemplateView
from .views import ElectricityDevicesView, ElectricityDeviceCreateView\
     , ElectricityDeviceUpdateView, ElectricityDeviceDeleteView, ElectricityUserDevicesView, ElectricityUserDevicesAddView\
    , ElectricityUserDevicesUpdateView, ElectricityUserDevicesDeleteView, ElectricityStatisticView, ElectricityUserDevicesCloneView

app_name = 'electricity'
urlpatterns = [
    path('', ElectricityDevicesView.as_view(), name='detail'),
    path('device_create', ElectricityDeviceCreateView.as_view(), name='device_create'),
    path('<int:device_id>/device_update', ElectricityDeviceUpdateView.as_view(), name='device_update'),
    path('<int:device_id>/device_delete', ElectricityDeviceDeleteView.as_view(), name='device_delete'),
    path('user_devices', ElectricityUserDevicesView.as_view(), name='user_devices'),
    path('user_devices/add/<int:device_id>', ElectricityUserDevicesAddView.as_view(), name='user_devices_add'),
    path('user_devices/update/<int:device_id>', ElectricityUserDevicesUpdateView.as_view(), name='user_devices_update'),
    path('user_devices/delete/<int:device_id>', ElectricityUserDevicesDeleteView.as_view(), name='user_devices_delete'),
    path('user_devices/clone/<int:device_id>', ElectricityUserDevicesCloneView.as_view(), name='user_devices_clone'),
    path('statistics', ElectricityStatisticView.as_view(), name='statistics'),
]