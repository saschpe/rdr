# -*- coding: utf-8 -*-

from models import Feed, Entry

from django.contrib import admin


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('feed', 'title', 'summary', 'link', 'author')
    list_filter  = list_display
    search_fields = list_display
    fieldsets = (
        (None,                  {'fields': ['feed', 'title', 'summary', 'link', 'author']}),
        ('Date information',    {'fields': ['published', 'updated'], 'classes': ['collapse']}),
        ('Caching information', {'fields': ['etag', 'modified'], 'classes': ['collapse']}),
    )


class EntryInline(admin.StackedInline):
    model = Entry
    fieldsets = EntryAdmin.fieldsets
    extra = 3


class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('url', 'version', 'title', 'subtitle', 'link')
    list_filter  = list_display
    search_fields= list_display
    fieldsets = (
        (None,               {'fields': ['url', 'version', 'title', 'subtitle', 'link']}),
        ('Date information', {'fields': ['updated'], 'classes': ['collapse']}),
    )
    inlines = (EntryInline,)


admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
