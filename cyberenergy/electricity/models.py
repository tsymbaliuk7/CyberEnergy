from django.core.validators import MinLengthValidator
from django.db import models
from datetime import time


class UserDevice(models.Model):
    device = models.ForeignKey('ElectricalDevices', on_delete=models.CASCADE, default=None)
    days = models.ForeignKey('DayOfWeek', default=None, on_delete=models.CASCADE, related_name='days_devices')
    start_time = models.TimeField(default=time(hour=0, minute=0))
    end_time = models.TimeField(default=time(hour=23, minute=59))


class ElectricalDevices(models.Model):
    name = models.CharField('Название', max_length=200,
                            validators=[MinLengthValidator(3, "Название прибора дожно состоять хотя бы с 3 символов")])
    power = models.DecimalField(default=None, decimal_places=3, max_digits=15)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, default=None)
    switch_on = models.ForeignKey('SwitchType', on_delete=models.CASCADE, default=None, related_name='switch_on_types')
    switch_off = models.ForeignKey('SwitchType', on_delete=models.CASCADE, default=None, related_name='switch_off_types')
    time_of_work = models.DecimalField(default=None, blank=True, null=True, max_digits=4, decimal_places=1)

    def __str__(self):
        return self.name


class SwitchType(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)

    def __str__(self):
        return self.name


class DayOfWeek(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)

    def __str__(self):
        return self.name
