# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response


def register(request):
    #TODO: Implement
    return render_to_response('accounts/register.html')
