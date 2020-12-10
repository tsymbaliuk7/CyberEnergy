from django.contrib import admin
from .models import DayOfWeek, ElectricalDevices, UserDevice, SwitchType

admin.site.register(DayOfWeek)
admin.site.register(ElectricalDevices)
admin.site.register(UserDevice)
admin.site.register(SwitchType)
