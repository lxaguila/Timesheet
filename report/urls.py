from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.views import logout
from django.conf import settings

app_name = 'report'

urlpatterns = [

    url(r'^$', login_required(views.WeekListView.as_view()), name='view_weeks'),
url(r'^week/$', login_required(views.WeekListView.as_view()), name='view_weeks_1'),
    url('^authenticate/$', views.UserFormView.as_view(), name='view_authenticate'),
    url('^day/add/(?P<pk>[0-9]+)$', login_required(views.CreateDay.as_view()), name = 'view_day_add'),
    url('^day/(?P<pk>[0-9]+)/delete/(?P<week>[0-9]+)/$', login_required(views.DeleteDay.as_view()), name = 'view_day_delete'),
    url('^day/(?P<pk>[0-9]+)/(?P<week>[0-9]+)/$', login_required(views.UpdateDay.as_view()), name='view_day_update'),

    url('^week/add/$', login_required(views.CreateWeek.as_view()), name='view_week_add'),
    url('^week/(?P<pk>[0-9]+)/delete/$', login_required(views.DeleteWeek.as_view()), name='view_week_delete'),
    url('^week/(?P<pk>[0-9]+)/$', login_required(views.WeekDetailView), name='view_week_detail'),
    url('^week/(?P<pk>[0-9]+)/update/$', login_required(views.UpdateWeek.as_view()), name='view_week_update'),

    url(r'^signout/$', logout, {'next_page': settings.LOGIN_URL}, name='logout')


    ]