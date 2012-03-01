# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^accounts/', include('apps.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^feeds/', include('apps.feeds.urls')),
    (r'^grappelli/', include('grappelli.urls')),
)
