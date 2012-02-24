# -*- coding: utf-8 -*-

from models import Feed, Subscription

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


@login_required
def index(request):
    subscriptions = request.user.subscription_set.all()
    return render_to_response('feeds/index.html', {'subscriptions': subscriptions}, context_instance=RequestContext(request))


@login_required
def show(request, feed_id):
    subscriptions = request.user.subscription_set.all()
    feed = get_object_or_404(Feed, pk=feed_id)
    return render_to_response('feeds/show.html', {'feed': feed, 'subscriptions': subscriptions}, context_instance=RequestContext(request))
