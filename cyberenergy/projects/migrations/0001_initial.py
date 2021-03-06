# Generated by Django 3.1.2 on 2020-11-05 17:12

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Region must be greater than 1 character')])),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(2, 'Название проекта дожно состоять хотя бы с 2 символов')], verbose_name='Название')),
                ('begin_date', models.DateField(default=datetime.date(2012, 1, 1), verbose_name='Дата начала')),
                ('end_date', models.DateField(default=datetime.date(2012, 12, 31), verbose_name='Дата конца')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_changed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.region')),
            ],
        ),
    ]
