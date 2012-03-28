# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns


urlpatterns = patterns('django.contrib.auth.views',
    (r'^login/$', 'login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'logout', {'template_name': 'accounts/logout.html'}),
    (r'^password_change/$', 'password_change', {'template_name': 'accounts/password_change.html'}),
    (r'^password_change/done/$', 'password_change_done', {'template_name': 'accounts/password_change_done.html'}),
    (r'^password_reset/$', 'password_reset', {'template_name': 'accounts/password_reset.html'}),
    (r'^password_reset/done/$', 'password_reset_done', {'template_name': 'accounts/password_reset_done.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'password_reset_confirm', {'template_name': 'accounts/reset.html'}),
    (r'^reset/done/$', 'password_reset_complete', {'template_name': 'accounts/reset_done.html'}),
)

urlpatterns += patterns('rdr.accounts.views',
    (r'^register/$', 'register'),
)
