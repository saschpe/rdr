# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('feeds.views',
    url(r'^$', 'index'),
    url(r'^(?<feed_id>\d+)/$', 'show'),
)
