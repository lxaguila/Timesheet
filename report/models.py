# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime


class weekly_report(models.Model):
    name = models.CharField(max_length=50)
    sent = models.BooleanField(default=False)
    total_hours = models.FloatField(default='0')
    total_miscelaneous = models.FloatField(default='0')
    comments = models.CharField(max_length=500, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('report:view_weeks')

    def __str__(self):
        return self.name


class daily_log(models.Model):
    week = models.ForeignKey(weekly_report, on_delete=models.CASCADE)
    start_date = models.DateField(default=now(), blank=False)
    start_time = models.TimeField(default="8:00am", blank=False)
    end_time = models.TimeField(default="5:00pm", blank=False)
    lunch_time = models.FloatField(default=0, blank=True, null=False)
    extra_time = models.FloatField(default=0, blank=True, null=False)
    travel_time = models.FloatField(default=0, blank=True, null=False)
    comments = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('report:view_week_update')

    def __str__(self):
        return unicode(self.start_date)

    @property
    def hours_worked(self):
        diff = (datetime.combine(self.start_date, self.end_time) - datetime.combine(self.start_date, self.start_time))
        return (diff.total_seconds()/3600) + self.travel_time - self.lunch_time + self.extra_time







