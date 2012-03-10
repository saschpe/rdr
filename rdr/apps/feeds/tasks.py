# -*- coding: utf-8 -*-

from celery.task import task
from models import Entry, Feed, Website


@task
def add(x, y):
    return x + y


@task
def create_feed_from_url(url, create_entries=True):
    return Feed.objects.create_from_url(url, create_entries)


@task
def update_feed(feed, update_entries=True):
    return feed.update(update_entries)


@task
def update_all_feeds(update_entries=True):
    for feed in Feed.objects.all():
        update_feed.delay(feed, update_entries)


@task
def create_website_from_url(url, create_entries=True):
    return Website.objects.create_from_url(url, create_entries)


@task
def update_website(website, update_title=False, update_entries=True):
    return website.update(update_title, update_entries)


@task
def update_all_websites(update_title=False, update_entries=True):
    for website in Website.objects.all():
        update_website.delay(website, update_title, update_entries)
