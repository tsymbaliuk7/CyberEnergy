from django.contrib import admin
from .models import DayOfWeek, ElectricalDevices, UserDevice, SwitchType, TariffRange, TariffZone, Tariff, ProjectZone

admin.site.register(DayOfWeek)
admin.site.register(ElectricalDevices)
admin.site.register(UserDevice)
admin.site.register(SwitchType)
admin.site.register(TariffRange)
admin.site.register(TariffZone)
admin.site.register(Tariff)
admin.site.register(ProjectZone)
