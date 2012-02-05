from django.db import models


class Feed(models.Model):
    TYPE_CHOICES = (
        (u'rss', u'RSS'),
        (u'atom', u'Atom'),
    )
    title = models.CharField(max_length=256)
    description = models.TextField()
    url = models.URLField()
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    updated_at = models.DateTimeField()


class Post(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    link = models.URLField()
    feed = models.ForeignKey(Feed)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
