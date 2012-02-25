# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}),
    (r'^register/$', 'apps.accounts.views.register'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change.html'}),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset.html'}),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/reset.html'}),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/reset_done.html'}),
)
