# Generated by Django 3.1.2 on 2020-11-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20201105_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='temperature',
            field=models.IntegerField(default=-20),
        ),
    ]
