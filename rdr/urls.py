# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from rdr.feeds.api import api_v1 as feed_api_v1

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^accounts/', include('rdr.accounts.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(feed_api_v1.urls)),
    (r'^feeds/', include('rdr.feeds.urls')),
    (r'^grappelli/', include('grappelli.urls')),
)
