# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import UserProfile
from rdr.feeds.models import SubscriptionInline, VisitedInline


admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, SubscriptionInline, VisitedInline)


admin.site.register(User, UserProfileAdmin)
