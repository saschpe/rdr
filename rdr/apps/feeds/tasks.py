# -*- coding: utf-8 -*-

from celery.task import task
from models import Entry, Feed


@task
def add(x, y):
    return x + y


@task
def create_feed_from_url(url, create_entries=True):
    return Feed.objects.create_from_url(url, create_entries)


@task
def update_feed(feed, update_entries=True):
    feed.update(update_entries)
    return feed


@task
def update_all_feeds(update_entries=True):
    for feed in Feed.objects.all():
        update_feed.delay(feed, update_entries)
