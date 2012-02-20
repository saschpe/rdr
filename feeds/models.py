# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

import feedparser

import datetime


class FeedManager(models.Manager):
    """Custom Feed model manager.

    Provides table-level methods to create Feed model objects from RSS/Atom 
    content fetched from a URL using the 'feedparser' Python module.
    """
    def get_or_create_from_url(self, url, create_entrys=True):
        try:
            return Feed.objects.get(url=url)
        except Feed.DoesNotExist:
            return self.create_from_url(url, create_entrys)

    def create_from_url(self, url, create_entrys=True):
        parsed = feedparser.parse(url)
        feed = Feed(
            url=parsed.href,
            version=parsed.version,
            title=parsed.feed.get('title', ''),
            subtitle=parsed.feed.get('subtitle', ''),
            link=parsed.feed.get('link', ''),
            etag=parsed.get('etag', ''),
        )
        if parsed.feed.has_key('updated_parsed'):
            feed.updated = datetime.datetime(*parsed.feed.updated_parsed[:6])
        if parsed.feed.has_key('modified_parsed'):
            feed.modified = datetime.datetime(*parsed.feed.modified_parsed[:6])
        feed.save()
        if create_entrys:
            Entry.objects.create_from_feed(feed, parsed)
        return feed


class Feed(models.Model):
    """Web feed model.

    The member / table column naming follows the Atom format.
    """
    TYPE_CHOICES = tuple(sorted(feedparser.SUPPORTED_VERSIONS.items()[1:]))

    url = models.URLField(unique=True)
    version = models.CharField(max_length=7, choices=TYPE_CHOICES, default=u'rss20')
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    link = models.URLField()
    updated = models.DateTimeField(null=True)

    etag = models.CharField(blank=True, max_length=64, editable=False) # HTTP ETag header
    modified = models.DateTimeField(null=True, editable=False) # HTTP Last-Modified header

    objects = FeedManager() # Custom model manager

    class Meta:
        ordering = ['title']

    def update(self):
        #TODO: Check for etag/last-modified headers when updating
        pass

    def __unicode__(self):
        return self.title


class EntryManager(models.Manager):
    """Custom Entry model manager.
    """
    #def get_or_create_from_feed(self, feed, parsed=None):
    #    #TODO
    #    pass

    def create_from_feed(self, feed, parsed=None):
        if parsed is None:
            parsed = feedparser.parse(feed.url)
        entrys = []
        for e in parsed.entries:
            entry = Entry(
                feed=feed,
                title=e.title,
                summary=e.get('summary', ''),
                content=e.get('content', ''),
                link=e.get('link', ''),
                author=e.get('author', ''),
            )
            if e.has_key('updated_parsed'):
                entry.updated = datetime.datetime(*e.updated_parsed[:6])
            if e.has_key('published_parsed'):
                entry.published = datetime.datetime(*e.published_parsed[:6])
            entry.save()
            entrys.append(entry)
        return entrys


class Entry(models.Model):
    """Web feed entry model.

    The member / table column naming follows the Atom format.
    """
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=256)
    summary = models.TextField()
    content = models.TextField(blank=True)
    link = models.URLField()
    author = models.CharField(blank=True, max_length=64)
    published = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)

    objects = EntryManager() # Custom model manager

    class Meta:
        ordering = ['published', 'title']

    def update(self):
        pass

    def __unicode__(self):
        return self.title


#class Subscription(models.Model):
#    user = models.ForeignKey(User)
#    feed = models.ForeignKey(Feed)
#    #custom_title = models.CharField(max_length=256)
#    unread_entrys = models.PositiveIntegerField()

#    class Meta:
#        ordering = ['user', 'feed']

#    def __unicode__(self):
#        return '{0} ({2})'.format(self.title, self.unread)
