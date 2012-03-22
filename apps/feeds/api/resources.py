# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from ..models import Website, Feed, Entry, Visited, Subscription


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']


class WebsiteResource(ModelResource):
    feed_set = fields.ToManyField('apps.feeds.api.resources.FeedResource', 'feed_set')

    class Meta:
        queryset = Website.objects.all()
        allowed_methods = ['get']


class FeedResource(ModelResource):
    website = fields.ToOneField(WebsiteResource, 'website', blank=True, null=True)
    entry_set = fields.ToManyField('apps.feeds.api.resources.EntryResource', 'entry_set')
    subscriber_set = fields.ToManyField('apps.feeds.api.resources.VisistedResource', 'subscriber_set')

    class Meta:
        queryset = Feed.objects.all()
        allowed_methods = ['get']


class EntryResource(ModelResource):
    feed = fields.ToOneField(FeedResource, 'feed')
    visitor_set = fields.ToManyField('apps.feeds.api.resources.VisistedResource', 'visitor_set')

    class Meta:
        queryset = Entry.objects.all()
        allowed_methods = ['get']


class VisistedResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    entry = fields.ToOneField(EntryResource, 'entry')

    class Meta:
        queryset = Visited.objects.all()
        allowed_methods = ['get']


class SubscriptionResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    feed = fields.ToOneField(FeedResource, 'feed')

    class Meta:
        queryset = Subscription.objects.all()
        allowed_methods = ['get']
