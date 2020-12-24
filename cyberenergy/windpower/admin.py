from django.contrib import admin
from .models import Windmill, WindmillTower, WindmillCharacteristics, WindmillType

# Register your models here.
admin.site.register(Windmill)
admin.site.register(WindmillTower)
admin.site.register(WindmillCharacteristics)
admin.site.register(WindmillType)
