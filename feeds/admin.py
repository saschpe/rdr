# -*- coding: utf-8 -*-

from models import Feed, Entry

from django.contrib import admin


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('feed', 'title', 'summary', 'link', 'author')
    list_filter  = ('feed', 'author')
    search_fields = ('title', 'summary', 'link', 'author')
    fieldsets = (
        (None,                  {'fields': ['feed', 'title', 'summary', 'link', 'author']}),
        ('Date information',    {'fields': ['published', 'updated'], 'classes': ['collapse']}),
        #('Caching information', {'fields': ['etag', 'modified'], 'classes': ['collapse']}),
    )


class EntryInline(admin.StackedInline):
    model = Entry
    fieldsets = EntryAdmin.fieldsets
    extra = 3


class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display   = ('url', 'title', 'subtitle', 'link')
    list_filter    = ('title', 'link')
    search_fields  = ('url', 'title', 'subtitle', 'link')
    fieldsets = (
        (None,               {'fields': ['url', 'title', 'subtitle', 'link']}),
        ('Date information', {'fields': ['updated'], 'classes': ['collapse']}),
    )
    inlines = (EntryInline,)


admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
