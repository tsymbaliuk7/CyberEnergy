import datetime

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2, "Region must be greater than 1 character")], unique=True
                            )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField('Название', max_length=200, unique=True,
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
        return reverse('projects:project', kwargs={'pk': self.pk})

    def set_is_changed(self, flag):
        self.is_changed = flag



