# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    #url(r'^reader/', include('reader.feeds.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^feeds/', include('feeds.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('accounts.urls')),
)
