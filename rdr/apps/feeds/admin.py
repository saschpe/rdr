# -*- coding: utf-8 -*-

from models import Entry, Feed, Visited, Subscription

from django.contrib import admin


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('feed', 'title', 'link', 'author')
    list_filter = ('feed', 'author')
    search_fields = ('title', 'summary', 'link', 'author')
    fieldsets = (
        (None,                  {'fields': ('feed', 'title', 'summary', 'link', 'author')}),
        ('Date information',    {'fields': ('published', 'updated'), 'classes': ('collapse')}),
        #('Caching information', {'fields': ('etag', 'modified'), 'classes': ('collapse')}),
    )


class EntryInline(admin.StackedInline):
    model = Entry
    fieldsets = EntryAdmin.fieldsets
    extra = 3


class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('url', 'title', 'subtitle', 'link')
    list_filter = ('title', 'link')
    search_fields = ('url', 'title', 'subtitle', 'link')
    fieldsets = (
        (None,               {'fields': ('url', 'title', 'subtitle', 'link')}),
        ('Date information', {'fields': ('updated',), 'classes': ('collapse')}),
    )
    inlines = (EntryInline,)


class VisitedAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry', 'marked')
    list_filter = ('user', 'entry')
    search_fields = ('user__username', 'entry__title')


class VisitedInline(admin.StackedInline):
    model = Visited
    fieldsets = VisitedAdmin.fieldsets
    extra = 5


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'feed', 'custom_feed_title')
    list_filter = ('user', 'feed')
    search_fields = ('user__username', 'feed__title')


class SubscriptionInline(admin.StackedInline):
    models = Subscription
    fieldsets = SubscriptionAdmin.fieldsets
    extra = 5


admin.site.register(Entry, EntryAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Visited, VisitedAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
