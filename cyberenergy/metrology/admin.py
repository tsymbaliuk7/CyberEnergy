from django.contrib import admin

from .models import Region, Metrology, MetrologyData, WindDirection, SolarData

admin.site.register(Region)
admin.site.register(Metrology)
admin.site.register(MetrologyData)
admin.site.register(WindDirection)
admin.site.register(SolarData)