# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.index', name='index'),
    #url(r'^reader/', include('reader.feeds.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^feeds/', include('feeds.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
