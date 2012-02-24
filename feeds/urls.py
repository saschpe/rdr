# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns('feeds.views',
    (r'^$', 'index'),
    (r'^(?P<feed_id>\d+)/$', 'show'),
)
