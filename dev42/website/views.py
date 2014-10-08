import datetime

from dev42.events.models import Event

from django.shortcuts import render

def homepage(request, homepage):

    return render(request, homepage.template, {
        'self': homepage,
        'current_event': Event.objects.filter(start_datetime__gt=datetime.datetime.now()).order_by('start_datetime').first()
    })