# -*- coding: utf-8 -*-

from models import Feed, Post

from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('feed', 'title', 'summary', 'link', 'author')
    list_filter  = list_display
    search_fields = list_display
    fieldsets = (
        (None,               {'fields': ['feed', 'title', 'summary', 'link', 'author']}),
        ('Date information', {'fields': ['published', 'updated'], 'classes': ['collapse']}),
    )


class PostInline(admin.StackedInline):
    model = Post
    fieldsets = PostAdmin.fieldsets
    extra = 3


class FeedAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('url', 'type', 'title', 'subtitle', 'link')
    list_filter  = list_display
    search_fields= list_display
    fieldsets = (
        (None,               {'fields': ['url', 'type', 'title', 'subtitle', 'link']}),
        ('Date information', {'fields': ['updated'], 'classes': ['collapse']}),
    )
    inlines = (PostInline,)


admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
