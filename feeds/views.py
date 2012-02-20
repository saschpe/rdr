# -*- coding: utf-8 -*-

from models import Feed

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404


def index(request):
    feeds = Feed.objects.all().order_by('-updated')[:20]
    return render_to_response('feeds/index.html', {'feeds': feeds})

def show(request):
    feed = get_object_or_404(Feed, pk=feed_id)
    return render_to_response('feeds/show.html', {'feed': feed})
