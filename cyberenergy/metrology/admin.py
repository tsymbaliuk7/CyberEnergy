from django.contrib import admin

from .models import MetrologyData, WindDirection, SolarData

admin.site.register(MetrologyData)
admin.site.register(WindDirection)
admin.site.register(SolarData)
