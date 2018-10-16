# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import daily_log
from .models import weekly_report

from django.contrib import admin

# Register your models here.

admin.site.register(daily_log)

admin.site.register(weekly_report)
