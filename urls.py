# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from tastypie.api import Api
from apps.feeds.api.resources import UserResource, WebsiteResource, FeedResource, EntryResource, VisistedResource, SubscriptionResource


# Create REST API:
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(WebsiteResource())
v1_api.register(FeedResource())
v1_api.register(EntryResource())
v1_api.register(VisistedResource())
v1_api.register(SubscriptionResource())

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^accounts/', include('apps.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^api/', include(v1_api.urls)),
    (r'^feeds/', include('apps.feeds.urls')),
    (r'^grappelli/', include('grappelli.urls')),
)
