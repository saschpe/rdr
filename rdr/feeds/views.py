# -*- coding: utf-8 -*-

from models import Feed, Subscription, Visited
from tasks import create_feed_from_url

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods


@login_required
def index(request):
    subscriptions = request.user.subscription_set.select_related().all()
    return render_to_response('feeds/index.html', {'subscriptions': subscriptions}, context_instance=RequestContext(request))


@login_required
def show(request, feed_id):
    subscriptions = request.user.subscription_set.select_related().all()
    feed = get_object_or_404(Feed, pk=feed_id)
    return render_to_response('feeds/show.html', {'feed': feed, 'subscriptions': subscriptions}, context_instance=RequestContext(request))


@login_required
@require_http_methods(('POST',))
def visit(request, feed_id):
    try:
        #TODO: Use bulk_create() once Django-1.4 hits the streets!
        Visited(user=request.user, entry_id=int(request.POST['entry'])).save()
    except KeyError:
        return HttpResponse('please provide an entry')
    except ValueError:
        return HttpResponse('please provide an entry id')
   #    for entry in request.POST['entries']:
   #        Visited(user=user,entry=entry).save()
    return redirect(show, int(feed_id))


@login_required
@require_http_methods(('POST',))
def subscribe(request):
    try:
        #feed = create_feed_from_url.delay(request.POST['url'])
        feed = Feed.objects.get_or_create_from_url(request.POST['url'])
        subscription = Subscription(user=request.user, feed=feed)
    except KeyError:
        return HttpResponse('please provide an entry')
    return redirect(index)
