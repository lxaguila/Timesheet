# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 03:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0016_auto_20181016_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_log',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2018, 10, 17, 3, 27, 4, 747551, tzinfo=utc)),
        ),
    ]