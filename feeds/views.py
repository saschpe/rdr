# -*- coding: utf-8 -*-

from models import Feed, Post

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404


def index(request):
    try:
        feeds = Feed.objects.all().order_by('-updated')[:5]
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('feeds/index.html', {'feeds': feeds})
