# Generated by Django 3.1.2 on 2020-11-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0004_auto_20201123_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='bath_water_volume',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='energy',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='q_bath',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='q_shower',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='shower_water_volume',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='total_water_volume',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=15, null=True),
        ),
    ]
