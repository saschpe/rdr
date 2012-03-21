# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns('apps.feeds.views',
    (r'^$', 'index'),
    (r'^(?P<feed_id>\d+)/$', 'show'),
    #(r'^(?P<feed_id>\d+)/entries/$', 'show'),
    #(r'^(?P<feed_id>\d+)/entries/(?P<entry_id>\d+)/$', 'show_entry'),
    (r'^(?P<feed_id>\d+)/visit/$', 'visit'),
    (r'^subscribe/$', 'subscribe'),
)
