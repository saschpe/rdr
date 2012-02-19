# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

import feedparser


class FeedManager(models.Manager):
    """Custom Feed model manager.
    """
    def get_or_create_from_url(self, url, create_posts=True):
        try:
            return Feed.objects.get(url=url)
        except Feed.DoesNotExist:
            return create_from_url(url, create_posts)

    def create_from_url(self, url, create_posts=True):
        parsed = feedparser.parse(url)
        feed = Feed(
            url=parsed.href,
            type=parsed.version,
            title=parsed.feed.title,
            subtitle=parsed.feed.subtitle,
            link=parsed.feed.link,
        )
        if parsed.feed.has_key('updated'):
            feed.updated = parsed.feed.updated
        feed.save()
        if create_posts:
            PostManager.create_from_feed(feed, parsed)
        return feed


class Feed(models.Model):
    """Web feed model.

    The member / table column naming follows the Atom format.
    """
    TYPE_CHOICES = (
        (u'rss090', u'RSS-0.9'),
        (u'rss100', u'RSS-1.0'),
        (u'rss20',  u'RSS-2.0'),
        (u'atom10', u'Atom-1.0'),
    )

    url = models.URLField(unique=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default=u'rss090')
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    link = models.URLField()
    updated = models.DateTimeField(blank=True)
    fetched = models.DateTimeField(auto_now=True, auto_now_add=True)

    objects = FeedManager() # Custom model manager

    class Meta:
        ordering = ['title']

    def update(self):
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
            post = Post(feed=feed, title=entry.title, summary=entry.summary, link=entry.link)
            if entry.has_key('content'):
                post.content = entry.content
            if entry.has_key('author'):
                post.author = entry.author
            if entry.has_key('updated'):
                post.updated = entry.updated
            if entry.has_key('published'):
                post.published = entry.published
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
    fetched = models.DateTimeField(auto_now=True, auto_now_add=True)

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
