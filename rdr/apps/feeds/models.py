# -*- coding: utf-8 -*-

import datetime
import feedparser
import logging
from django.contrib.auth.models import User
from django.db import models


logger = logging.getLogger(__name__)


class FeedManager(models.Manager):
    '''Custom Feed model manager.

    Provides table-level methods to create Feed model objects from RSS/Atom
    files fetched from a URL using the 'feedparser' Python module.
    '''
    def update_or_create_from_url(self, url, update_entries=True):
        try:
            return Feed.objects.get(url=url).update(update_entries)
        except Feed.DoesNotExist:
            return self.create_from_url(url, update_entries)

    def create_from_url(self, url, create_entries=True):
        parsed = feedparser.parse(url)
        feed = Feed(
            url=parsed.href,
            title=parsed.feed.get('title', ''),
            subtitle=parsed.feed.get('subtitle', ''),
            link=parsed.feed.get('link', ''),
        )
        if 'updated_parsed' in parsed.feed:
            feed.updated = datetime.datetime(*parsed.feed.updated_parsed[:6])
        if 'etag' in parsed.feed:
            feed.etag = parsed.feed.etag
        if 'modified_parsed' in parsed.feed:
            feed.modified = datetime.datetime(*parsed.feed.modified_parsed[:6])
        logger.debug('feed "{0}" created'.format(feed))
        feed.save()
        if create_entries:
            for parsed_entry in parsed.entries:
                Entry.objects.create_from_feed_and_parsed_entry(self, feed, parsed_entry)
        return feed


class Feed(models.Model):
    '''Web feed model.

    The member / table column naming follows the Atom format.
    '''
    url = models.URLField(unique=True)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    link = models.URLField()
    updated = models.DateTimeField(null=True)
    etag = models.CharField(null=True, max_length=64, editable=False)  # HTTP ETag header
    modified = models.DateTimeField(null=True, editable=False)  # HTTP Last-Modified header
    subscribers = models.ManyToManyField(User, through='Subscription')  # User Feed subscriptions
    objects = FeedManager()  # Custom model manager

    def update(self, update_entries=True):
        '''Update the feed model instance.
        
        Requests the Atom/RSS file from the upstream feed URL and parses the results.
        Honors HTTP Etag and Last-Modified headers (when available) to avoid fetching unchanged files.
        The model instance is only stored to the database if it really changed.
        '''
        parsed = feedparser.parse(self.url, etag=self.etag, modified=self.modified)
        if parsed.status == 304:  # Unmodified file, nothing to do
            logger.debug('feed "{0}" unmodified'.format(self))
            return
        
        # Get items from parsed feed and check if the underlying model changed...
        feed_changed = False
        parsed_title = parsed.feed.get('title', '')
        if self.title != parsed_title:
            self.title, feed_changed = parsed_title, True
        parsed_subtitle = parsed.feed.get('subtitle', '')
        if self.subtitle != parsed_subtitle:
            self.subtitle, feed_changed = parsed_subtitle, True
        parsed_link = parsed.feed.get('link', '')
        if self.link != parsed_link:
            self.link, feed_changed = parsed_link, True
        if 'updated_parsed' in parsed.feed:
            parsed_updated = datetime.datetime(*parsed.feed.updated_parsed[:6])
            if self.updated != parsed_updated:
                self.updated, feed_changed = parsed_updated, True
        if 'etag' in parsed.feed and self.etag != parsed.feed.etag:
            self.etag, feed_changed = parsed.feed.etag, True
        if 'modified_parsed' in parsed.feed:
            parsed_modified = datetime.datetime(*parsed.feed.modified_parsed[:6]) 
            if self.modified != parsed_modified:
                self.modified, feed_changed = parsed_modified, True

        if feed_changed: # Only save Feed model if it really changed
            logger.debug('feed "{0}" updated'.format(self))
            self.save()
        if update_entries: # Not 'feed_changed' doesn't mean that entries didn't change
            for parsed_entry in parsed.entries:
                Entry.objects.update_or_create_from_feed_and_parsed_entry(self, parsed_entry)

    def __unicode__(self):
        return self.title


class EntryManager(models.Manager):
    '''Custom Entry model manager.

    Provides table-level methods to create Entry model objects from RSS/Atom
    files fetched from a URL using the 'feedparser' Python module.
    '''
    def update_or_create_from_feed_and_parsed_entry(self, feed, parsed_entry):
        try:
            return Entry.objects.get(feed=feed, link=parsed_entry.link).update(parsed_entry)
        except Entry.DoesNotExist:
            return self.create_from_feed_and_parsed_entry(feed, parsed_entry)

    def create_from_feed_and_parsed_entry(self, feed, parsed_entry):
        '''Create an Entry model instance from a parsed web feed entry for a Feed instance.
        '''
        entry = Entry(
            feed=feed,
            title=parsed_entry.title,
            summary=parsed_entry.get('summary', ''),
            link=parsed_entry.link,
            author=parsed_entry.get('author', ''),
        )
        if 'updated_parsed' in parsed_entry:
            entry.updated = datetime.datetime(*parsed_entry.updated_parsed[:6])
        if 'published_parsed' in parsed_entry:
            entry.published = datetime.datetime(*parsed_entry.published_parsed[:6])
        logger.debug('feed "{0}" entry "{1}" created"'.format(feed, entry))
        entry.save()
        return entry


class Entry(models.Model):
    '''Web feed entry model.

    The member / table column naming follows the Atom format.
    '''
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=256)
    summary = models.TextField()
    link = models.URLField()
    author = models.CharField(blank=True, max_length=64)
    published = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)
    objects = EntryManager()  # Custom model manager

    class Meta:
        unique_together = (('feed', 'link'))

    def update(self, parsed_entry):
        '''Update the Entry model instance.

        The model instance is only stored to the database if it really changed.
        '''
        entry_changed = False
        if self.title != parsed_entry.title:
            self.title, entry_changed = parsed_entry.title, True
        if self.summary != parsed_entry.get('summary', ''):
            self.summary, entry_changed = parsed_entry.get('summary', ''), True
        if self.link != parsed_entry.get('link', ''):
            self.link, entry_changed = parsed_entry.get('link', ''), True
        if self.author != parsed_entry.get('author', ''):
            self.author, entry_changed = parsed_entry.get('author', ''), True
        if 'updated_parsed' in parsed_entry:
            parsed_updated = datetime.datetime(*parsed_entry.updated_parsed[:6])
            if self.updated != parsed_updated:
                self.updated, entry_changed = parsed_updated, True
        if 'published_parsed' in parsed_entry:
            parsed_published = datetime.datetime(*parsed_entry.published_parsed[:6])
            if self.published != parsed_published:
                self.published, entry_changed = parsed_published, True

        if entry_changed: # Only save Entry model if it actually changed
            logger.debug('feed "{0}" entry "{1}" updated"'.format(self.feed, self))
            self.save()

    def __unicode__(self):
        return self.link


class ReadEntry(models.Model):
    '''
    '''
    subscription = models.ForeignKey('Subscription')
    entry = models.ForeignKey(Entry)
    marked = models.BooleanField(default=False)

    class Meta:
        ordering = ('subscription', 'entry')
        unique_together = (('subscription', 'entry'))

    def __unicode__(self):
        return '{0} - {1}'.format(self.subscription, self.entry)


class Subscription(models.Model):
    '''User subscription to a feed M2M relationship.

    Stores a custom feed title that be set by the user. Unread entries are
    stored directly as a counter and only read entries have a real M2M
    relationship.

    This should be fastest when a new subscription is added, the amount of
    unread entries equals all entries of a given feed. The 'read' M2M
    relationship goes through the 'ReadEntry' model that allows to store
    additional user-saved data (like a bookmarked state or a comment).
    '''
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    custom_feed_title = models.CharField(blank=True, max_length=256)
    read_entries = models.ManyToManyField(Entry, through='ReadEntry')
    unread_entries = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('user', 'feed')
        unique_together = (('user', 'feed'))

    def __unicode__(self):
        return '{0} - {1}'.format(self.user, self.feed)
