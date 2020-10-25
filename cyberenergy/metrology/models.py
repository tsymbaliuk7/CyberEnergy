from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils.timezone import now
from django.urls import reverse
import datetime


class Region(models.Model):
    name = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2, "Region must be greater than 1 character")]
                            )

    def __str__(self):
        return self.name


class Metrology(models.Model):
    name = models.CharField('Название', max_length=200,
                            validators=[MinLengthValidator(2, "Название проекта дожно состоять хотя бы с 2 символов")])
    begin_date = models.DateField('Дата начала', default=datetime.date(2012, 1, 1))
    end_date = models.DateField('Дата конца', default=datetime.date(2012, 12, 31))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_changed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('metrology:project', kwargs={'pk': self.pk})

    def set_is_changed(self, flag):
        self.is_changed = flag


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
    metrology = models.ForeignKey(Metrology, on_delete=models.CASCADE)


class SolarData(models.Model):
    date = models.DateTimeField()
    value = models.IntegerField()
    metrology = models.ForeignKey(Metrology, on_delete=models.CASCADE)