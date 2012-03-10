# -*- coding: utf-8 -*-

from models import Entry, Feed, Subscription, Visited, Website

from django.contrib import admin


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('feed', 'title', 'link', 'author')
    list_filter = ('feed', 'author')
    search_fields = ('feed__title', 'title', 'summary', 'link', 'author')
    fieldsets = (
        (None,                  {'fields': ('feed', 'title', 'summary', 'link', 'author')}),
        ('Date information',    {'fields': ('published', 'updated'), 'classes': ('collapse')}),
    )


class EntryInline(admin.StackedInline):
    model = Entry
    fieldsets = EntryAdmin.fieldsets
    extra = 0


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'feed', 'custom_feed_title')
    list_filter = ('user', 'feed')
    search_fields = ('user__username', 'feed__title')


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    fieldsets = SubscriptionAdmin.fieldsets


class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('url', 'title', 'subtitle', 'link', 'website')
    list_filter = ('title', 'link', 'website')
    search_fields = ('url', 'title', 'subtitle', 'link', 'website__title')
    fieldsets = (
        (None,               {'fields': ('url', 'title', 'subtitle', 'link', 'website')}),
        ('Date information', {'fields': ('updated',), 'classes': ('collapse')}),
    )
    inlines = (EntryInline, SubscriptionInline)


class FeedInline(admin.StackedInline):
    model = Feed
    fieldsets = FeedAdmin.fieldsets
    extra = 0


class VisitedAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry', 'marked')
    list_filter = ('user', 'entry', 'marked')
    search_fields = ('user__username', 'entry__title')


class VisitedInline(admin.StackedInline):
    model = Visited
    fieldsets = VisitedAdmin.fieldsets


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')
    search_fields = ('url', 'title')
    inlines = (FeedInline,)


admin.site.register(Entry, EntryAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Visited, VisitedAdmin)
admin.site.register(Website, WebsiteAdmin)
