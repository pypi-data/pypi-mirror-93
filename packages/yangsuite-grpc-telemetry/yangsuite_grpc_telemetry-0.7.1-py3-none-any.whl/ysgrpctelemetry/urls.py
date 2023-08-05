# Copyright 2016 Cisco Systems, Inc
from django.conf.urls import url
from . import views

app_name = 'grpctelemetry'
urlpatterns = [
    url(r'^$', views.render_main_page, name="main"),
    url(r'^servicer/(?P<port>[0-9]+)/start?$', views.start_servicer,
        name="start_servicer"),
    url(r'^servicer/(?P<port>[0-9]+)/output?$', views.get_output,
        name="get_output"),
    url(r'^servicer/(?P<port>[0-9]+)/stop?$', views.stop_servicer,
        name="stop_servicer"),
]
