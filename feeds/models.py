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
    def get_or_create_by_url(self, url, create_entrys=True):
        try:
            return Feed.objects.get(url=url)
        except Feed.DoesNotExist:
            return self.create_by_url(url, create_entrys)

    def create_by_url(self, url, create_entrys=True):
        parsed = feedparser.parse(url)
        feed = Feed(
            url=parsed.href,
            title=parsed.feed.get('title', ''),
            subtitle=parsed.feed.get('subtitle', ''),
            link=parsed.feed.get('link', ''),
        )
        if parsed.feed.has_key('updated_parsed'):
            feed.updated = datetime.datetime(*parsed.feed.updated_parsed[:6])
        if parsed.feed.has_key('etag'):
            feed.etag = parsed.feed.etag
        if parsed.feed.has_key('modified_parsed'):
            feed.modified = datetime.datetime(*parsed.feed.modified_parsed[:6])
        feed.save()
        if create_entrys:
            for parsed_entry in parsed.entries:
                Entry.objects.create_by_feed_and_parsed_entry(self, feed, parsed_entry)
        return feed


class Feed(models.Model):
    """Web feed model.

    The member / table column naming follows the Atom format.
    """
    url = models.URLField(unique=True)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    link = models.URLField()
    updated = models.DateTimeField(null=True)

    etag = models.CharField(null=True, max_length=64, editable=False) # HTTP ETag header
    modified = models.DateTimeField(null=True, editable=False) # HTTP Last-Modified header

    subscribers = models.ManyToManyField(User, through='Subscription')

    objects = FeedManager() # Custom model manager

    def update_by_url(self, create_entrys=True):
        """Update the Feed instance from it's web feed URL.

        Honors HTTP Etag and Last-Modified headers to avoid fetching unchanged content.
        """
        parsed = feedparser.parse(url, etag=feed.etag, modified=feed.modified)
        if parsed.status == 304: # Unmodified content, nothing to do
            return

        self.title = parsed.feed.get('title', ''),
        self.subtitle = parsed.feed.get('subtitle', ''),
        self.link = parsed.feed.get('link', ''),
        if parsed.feed.has_key('updated_parsed'):
            self.updated = datetime.datetime(*parsed.feed.updated_parsed[:6])
        if parsed.feed.has_key('etag'):
            self.etag = parsed.feed.etag
        if parsed.feed.has_key('modified_parsed'):
            self.modified = datetime.datetime(*parsed.feed.modified_parsed[:6])
        self.save()
        if create_entrys:
            for parsed_entry in parsed.entries:
                Entry.objects.get_or_create_by_feed_and_parsed_entry(self, feed, parsed_entry)

    def __unicode__(self):
        return self.title


class EntryManager(models.Manager):
    """Custom Entry model manager.

    Provides table-level methods to create Entry model objects from RSS/Atom
    content fetched from a URL using the 'feedparser' Python module.
    """
    def get_or_create_by_feed_and_parsed_entry(self, feed, parsed_entry):
        try:
            return Entry.objects.get(feed=feed, title=parsed_entry.title)
        except Entry.DoesNotExist:
            return self.create_by_feed_and_parsed_entry(self, feed, parsed_entry)

    def create_by_feed_and_parsed_entry(self, feed, parsed_entry):
        """Create an Entry model instance from a parsed web feed entry for a Feed instance.
        """
        entry = Entry(
            feed=feed,
            title=parsed_entry.title,
            summary=parsed_entry.get('summary', ''),
            content=parsed_entry.get('content', ''),
            link=parsed_entry.get('link', ''),
            author=parsed_entry.get('author', ''),
        )
        if parsed_entry.has_key('updated_parsed'):
            entry.updated = datetime.datetime(*parsed_entry.updated_parsed[:6])
        if parsed_entry.has_key('published_parsed'):
            entry.published = datetime.datetime(*parsed_entry.published_parsed[:6])
        entry.save()
        return entry


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

    def __unicode__(self):
        return self.title


class Subscription(models.Model):
    """User subscription to a Feed join-table.

    Stores a custom Feed title that be set by the user.
    """
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    custom_feed_title = models.CharField(null=True, blank=True, max_length=256)
    #unread_entrys = models.PositiveIntegerField()

    class Meta:
        ordering = ['user', 'feed']
        unique_together = (('user', 'feed'))

    def __unicode__(self):
        return '{0} - {1}'.format(self.user, self.feed)
