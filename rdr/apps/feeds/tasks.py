# -*- coding: utf-8 -*-

from celery.task import task
from models import Entry, Feed


@task
def add(x, y):
    return x + y


@task
def create_feed_from_url(url, create_entries=True):
    return Feed.create_feed_from_url(url, create_entries)


@task
def update_feed(feed, create_entries=True):
    feed.update(create_entries)
    return feed
