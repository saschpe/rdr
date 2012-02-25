# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns('apps.feeds.views',
    (r'^$', 'index'),
    (r'^(?P<feed_id>\d+)/$', 'show'),
)
