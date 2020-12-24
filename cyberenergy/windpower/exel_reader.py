import os
import pandas as pd
import csv
import operator
import datetime
from calendar import monthrange
from .models import *
from pytz import timezone
import numpy as np
from django.apps import apps
import random


def exel_reader(obj):
    WindDirection = apps.get_model('metrology', 'WindDirection')
    MetrologyData = apps.get_model('metrology', 'MetrologyData')
    SolarData = apps.get_model('metrology', 'SolarData')
    month_s = obj.begin_date.month
    month_e = obj.end_date.month
    reg = obj.region.name
    proj_dir = os.getcwd()
    os.chdir('metrology/ukrdb/{0}'.format(reg.lower().replace(' ', '')))
    files = list(os.listdir('.'))
    all_file_frames = []
    file_dict = dict(zip(files, [int(f.split('-')[1].split('.')[0]) for f in files]))
    file_dict = sorted(file_dict.items(), key=operator.itemgetter(1))
    for key, item in file_dict:
        if month_s <= item <= month_e:
            temp = pd.read_excel(key, header=0)
            temp.insert(11, 'month', item)
            all_file_frames.append(temp)
    all_frame = pd.concat(all_file_frames, axis=0)
    os.chdir(proj_dir)
    all_frame.to_csv('Result.csv')
    fhand = open('Result.csv', encoding='utf-8')
    reader = csv.reader(fhand)
    next(reader)
    new_data = []
    for row in reader:
        try:
            t = float(row[3])
        except:
            t = 0

        s = row[4]
        if s == '':
            s = 'Штиль'

        try:
            v = int(row[5])
        except:
            v = 0
        if monthrange(2012, int(row[12]))[1] >= int(row[1]):
            date = datetime.datetime(day=int(row[1]), month=int(row[12]), year=2012, hour=int(row[2].split(':')[0]),
                                     minute=int(row[2].split(':')[1]), tzinfo=timezone('UTC'))
            if obj.begin_date <= date.date() <= obj.end_date:
                new_data.append([date, t, s, v])
    missed_data = []
    del_data = []
    for i in range(len(new_data) - 1):
        if new_data[i + 1][0] - new_data[i][0] != datetime.timedelta(minutes=30):
            if new_data[i][0].day == new_data[i + 2][0].day and new_data[i + 1][0].day != new_data[i][0].day:
                new_data[i + 1][0] = new_data[i + 1][0].replace(day=new_data[i][0].day)
            elif new_data[i][0] == new_data[i + 1][0]:
                del_data.append(i + 1)
            else:
                dif = new_data[i + 1][0] - new_data[i][0]
                step = int(dif / datetime.timedelta(minutes=30)) - 1
                if step == 1:
                    temp = new_data[i][0] + datetime.timedelta(minutes=30)
                    missed_data.append([temp, new_data[i][1], new_data[i][2], new_data[i][3]])
                elif step % 2 == 0:
                    for j in range(int(step / 2)):
                        temp = new_data[i][0] + datetime.timedelta(minutes=(j + 1) * 30)
                        missed_data.append([temp, new_data[i][1], new_data[i][2], new_data[i][3]])
                        temp = new_data[i + 1][0] - datetime.timedelta(minutes=(j + 1) * 30)
                        missed_data.append([temp, new_data[i + 1][1], new_data[i + 1][2], new_data[i + 1][3]])
                else:
                    for j in range(int(step / 2)):
                        temp = new_data[i][0] + datetime.timedelta(minutes=(j + 1) * 30)
                        missed_data.append([temp, new_data[i][1], new_data[i][2], new_data[i][3]])
                        temp = new_data[i + 1][0] - datetime.timedelta(minutes=(j + 1) * 30)
                        missed_data.append([temp, new_data[i + 1][1], new_data[i + 1][2], new_data[i + 1][3]])
                        temp = new_data[i][0] + datetime.timedelta(minutes=(j + 1) * 30)
                        missed_data.append([temp, new_data[i][1], new_data[i][2], new_data[i][3]])

    for index in del_data:
        del new_data[index]
    for elem in missed_data:
        new_data.append(elem)

    for elem in new_data:
        w, created = WindDirection.objects.get_or_create(name=elem[2])
        w.save()
        m, created = MetrologyData.objects.get_or_create(wind_direction=w, date=elem[0], metrology=obj,
                                                         temperature=elem[1],
                                                         wind_speed=elem[3])
        m.save()

    os.chdir('metrology/ukrdb')
    fhand = open('newyork.csv', encoding='utf-8')
    os.chdir(proj_dir)
    reader = csv.reader(fhand)
    next(reader)
    next(reader)
    solar_data = []
    for rows in reader:
        month_day = rows[0].split('/')
        month_day = [int(i) for i in month_day]
        hour = int(rows[1].split(':')[0])
        if hour == 24:
            new_date = datetime.date(year=2012, month=month_day[0], day=month_day[1]) + datetime.timedelta(days=1)
            if new_date.year == 2013:
                new_date = datetime.date(year=2012, month=new_date.month, day=new_date.day)
            month_day = [new_date.month, new_date.day]
            hour = 0
        date = datetime.datetime(year=2012, month=month_day[0], day=month_day[1], hour=hour,
                                 minute=0, tzinfo=timezone('UTC'))
        etrn = int(rows[3])
        if etrn > 0 and (obj.begin_date <= date.date() <= obj.end_date):
            solar_data.append([date, etrn])
            if month_day[0] == 2 and month_day[1] == 28:
                date = date + datetime.timedelta(days=1)
                solar_data.append([date, int(rows[3])])
    for elem in solar_data:
        sd, created = SolarData.objects.get_or_create(date=elem[0], value=elem[1], metrology=obj)
        sd.save()


def fill_wind_characteristics(max_value):
    result = []
    for i in range(1, 3):
        result.append(0)
    choice = random.choice([i for i in range(17, 22)])
    rand = np.logspace(np.log(5), np.log(max_value), choice, base=np.exp(1))
    rand = [round(i, 2) for i in rand]
    for r in rand:
        result.append(r)
    if len(result) - 1 < 25:
        for i in range(0, 25 - len(result) + 1):
            result.append(max_value)
    result = dict(zip(list(range(1, 26)), result))
    return result
