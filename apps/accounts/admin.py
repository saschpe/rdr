# -*- coding: utf-8 -*-

from models import UserProfile
from apps.feeds.models import SubscriptionInline, VisitedInline

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, SubscriptionInline, VisitedInline)


admin.site.register(User, UserProfileAdmin)
