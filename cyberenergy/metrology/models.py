from django.db import models


class WindDirection(models.Model):
    name = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name


class MetrologyData(models.Model):
    date = models.DateTimeField()
    temperature = models.DecimalField(decimal_places=1, max_digits=4)
    wind_direction = models.ForeignKey(WindDirection, on_delete=models.CASCADE)
    wind_speed = models.IntegerField(default=0)
    metrology = models.ForeignKey('projects.Project', on_delete=models.CASCADE)


class SolarData(models.Model):
    date = models.DateTimeField()
    value = models.IntegerField()
    metrology = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
