# Generated by Django 3.1.2 on 2020-11-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_auto_20201123_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='coal_price',
            field=models.DecimalField(decimal_places=2, default=3500, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='electrical_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='energy_price',
            field=models.DecimalField(decimal_places=3, default=1600, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='gaz_price',
            field=models.DecimalField(decimal_places=2, default=8.8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='pellets_price',
            field=models.DecimalField(decimal_places=2, default=6000, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='wood_price',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10, null=True),
        ),
    ]
