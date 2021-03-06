from django.db import models


class House(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    heat_loss = models.DecimalField(default=100, decimal_places=2, max_digits=10)
    area = models.DecimalField(default=None, decimal_places=1, max_digits=6)
    residents = models.PositiveIntegerField(default=None)
    water_start_temperature = models.DecimalField(default=15, decimal_places=1, max_digits=6)
    water_end_temperature = models.DecimalField(default=85, decimal_places=1, max_digits=6)
    water_shower_temperature = models.DecimalField(default=40, decimal_places=1, max_digits=6)
    shower_number = models.PositiveIntegerField(default=None)
    water_bath_temperature = models.DecimalField(default=40, decimal_places=1, max_digits=6)
    bath_number = models.PositiveIntegerField(default=None)
    heating_duration = models.DecimalField(default=None, decimal_places=1, max_digits=4, blank=True)
    heater_power = models.DecimalField(default=None, decimal_places=4, max_digits=15, blank=True)
    expected_air_temperature = models.DecimalField(default=20, decimal_places=1, max_digits=6)
    shower_water_volume = models.DecimalField(default=None, decimal_places=3, max_digits=15, null=True)
    bath_water_volume = models.DecimalField(default=None, decimal_places=3, max_digits=15, null=True)
    total_water_volume = models.DecimalField(default=None, decimal_places=3, max_digits=15, null=True)
    q_shower_normal = models.DecimalField(default=150, decimal_places=1, max_digits=10, blank=True)
    q_bath_normal = models.DecimalField(default=75, decimal_places=1, max_digits=10, blank=True)
    q_shower = models.DecimalField(default=None, decimal_places=1, max_digits=10, null=True)
    q_bath = models.DecimalField(default=None, decimal_places=1, max_digits=10, null=True)
    energy = models.DecimalField(default=None, decimal_places=1, max_digits=10, null=True)
    energy_price = models.DecimalField(default=1600, decimal_places=3, max_digits=10, null=True)
    gaz_price = models.DecimalField(default=8.8, decimal_places=2, max_digits=10, null=True)
    coal_price = models.DecimalField(default=3500, decimal_places=2, max_digits=10, null=True)
    wood_price = models.DecimalField(default=1000, decimal_places=2, max_digits=10, null=True)
    pellets_price = models.DecimalField(default=6000, decimal_places=2, max_digits=10, null=True)
    electrical_price = models.DecimalField(default=1, decimal_places=2, max_digits=10, null=True)