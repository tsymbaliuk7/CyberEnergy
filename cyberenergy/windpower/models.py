from django.core.validators import MinLengthValidator
from django.db import models


class Windmill(models.Model):
    name = models.CharField('Название', max_length=200,
                            validators=[MinLengthValidator(3, "Тип ветряка дожен состоять хотя бы с 3 символов")],
                            default=None)
    type = models.ForeignKey('WindmillType', on_delete=models.CASCADE, default=None)
    price = models.DecimalField(default=None, max_digits=10, decimal_places=2)
    project = models.ForeignKey('projects.Project', default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'project'),)

    def __str__(self):
        return self.name


class WindmillTower(models.Model):
    height = models.DecimalField(default=None, max_digits=10, decimal_places=3)
    price = models.DecimalField(default=None, max_digits=10, decimal_places=2)
    windmill = models.ForeignKey(Windmill, default=None, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('windmill', 'height',)

    def __str__(self):
        return 'Башня {} м. ({})'.format(round(self.height), self.windmill)


class WindmillCharacteristics(models.Model):
    windspeed = models.IntegerField(default=None)
    power = models.DecimalField(default=None, max_digits=10, decimal_places=3)
    windmill = models.ForeignKey(Windmill, default=None, on_delete=models.CASCADE)


class WindmillType(models.Model):
    name = models.CharField('Название', max_length=200,
                            validators=[MinLengthValidator(3, "Тип ветряка дожен состоять хотя бы с 3 символов")],
                            default=None)

    def __str__(self):
        return self.name
