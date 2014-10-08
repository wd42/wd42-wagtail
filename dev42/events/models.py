from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel

class ScheduleItem(models.Model):
    title = models.CharField(max_length=255)
    time = models.TimeField()
    speaker = models.CharField(max_length=255, blank=True)

    page = ParentalKey('events.Event', related_name='schedule')

    panels = [
        FieldPanel('time'),
        FieldPanel('title'),
        FieldPanel('speaker'),
    ]

    class Meta:
        ordering = ['time']

class EventIndex(Page):
    subpage_types = ['Event']

class Event(Page):
    start_datetime = models.DateTimeField('Start')
    end_datetime = models.DateTimeField('End')
    signup_link = models.URLField(blank=True)

    subpage_types = []
    parent_page_types = ['EventIndex']

Event.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('signup_link'),
    InlinePanel( Event, 'schedule', label="Schedule" ),
    MultiFieldPanel([FieldRowPanel([
        FieldPanel('start_datetime', classname='col6'),
        FieldPanel('end_datetime', classname='col6'),
    ])], 'Dates'),
]