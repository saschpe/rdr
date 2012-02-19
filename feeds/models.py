# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

import feedparser

from datetime import datetime


class FeedManager(models.Manager):
    """Custom Feed model manager.

    Provides table-level methods to create Feed model objects from RSS/Atom 
    content fetched from a URL using the 'feedparser' Python module.
    """
    def get_or_create_from_url(self, url, create_posts=True):
        try:
            return Feed.objects.get(url=url)
        except Feed.DoesNotExist:
            return self.create_from_url(url, create_posts)

    def create_from_url(self, url, create_posts=True):
        parsed = feedparser.parse(url)
        feed = Feed(
            url=parsed.href,
            version=parsed.version,
            title=parsed.feed.get('title', ''),
            subtitle=parsed.feed.get('subtitle', ''),
            link=parsed.feed.get('link', ''),
            etag=parsed.get('etag', ''),
            modified=parsed.get('modified', ''),
        )
        if parsed.feed.has_key('updated_parsed'):
            feed.updated = datetime(*parsed.feed.updated_parsed[:6])
       #if parsed.feed.has_key('icon'):
       #    feed.image = 
       #elif parsed.feed.has_key('logo'):
       #    pass
       #elif parsed.feed.has_key('image'):
       #    pass
        feed.save()
        if create_posts:
            PostManager.create_from_feed(feed, parsed)
        return feed


class Feed(models.Model):
    """Web feed model.

    The member / table column naming follows the Atom format.
    """
    TYPE_CHOICES = tuple(feedparser.SUPPORTED_VERSIONS.items()[1:])

    url = models.URLField(unique=True)
    version = models.CharField(max_length=7, choices=TYPE_CHOICES, default=u'rss20')
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    link = models.URLField()
    updated = models.DateTimeField(blank=True)
    etag = models.CharField(max_length=64, editable=False) # HTTP ETag header
    modified = models.DateTimeField(editable=False) # HTTP Last-Modified header
    #fetched = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = FeedManager() # Custom model manager

    class Meta:
        ordering = ['title']

    def update(self):
        #TODO: Check for etag/last-modified headers when updating
        pass

    def __unicode__(self):
        return '{0} {1}'.format(self.title, self.url)


class PostManager(models.Manager):
    """Custom Post model manager.
    """
    #def get_or_create_from_feed(self, feed, parsed=None):
    #    #TODO
    #    pass

    def create_from_feed(self, feed, parsed=None):
        if parsed is None:
            parsed = feedparser.parse(feed.url)
        posts = []
        for entry in parsed.entries:
            post = Post(
                feed=feed,
                title=entry.title,
                summary=entry.get('summary', ''),
                content=entry.get('content', ''),
                link=entry.get('link', ''),
                author=entry.get('author', ''),
            )
            if entry.has_key('updated_parsed'):
                post.updated = datetime(*entry.updated_parsed[:6])
            if entry.has_key('published_parsed'):
                post.published = datetime(*entry.published_parsed[:6])
            post.save()
            posts.append(post)
        return posts


class Post(models.Model):
    """Web feed entry model.

    The member / table column naming follows the Atom format.
    """
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=256)
    summary = models.TextField()
    content = models.TextField(blank=True)
    link = models.URLField()
    author = models.CharField(blank=True, max_length=64)
    published = models.DateTimeField(blank=True)
    updated = models.DateTimeField(blank=True)
    #fetched = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = PostManager() # Custom model manager

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
#    unread_posts = models.PositiveIntegerField()

#    class Meta:
#        ordering = ['user', 'feed']

#    def __unicode__(self):
#        return '{0} ({2})'.format(self.title, self.unread)
