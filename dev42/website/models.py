from django.db import models
from django.shortcuts import render

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.models import Image
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

from modelcluster.fields import ParentalKey

from dev42.utils.views import ModelViewProxy

views = ModelViewProxy('dev42.website.views')

COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
)


class ContentPage(Page):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = None

ContentPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]

ContentPage.promote_panels = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
]


class Sponsor(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()

    # Must be `null=True, on_delete=models.SET_NULL` to prevent cascading
    # deletion when the image is removed. `blank=False` makes it required when
    # adding/editing it through forms though.
    logo = models.ForeignKey(Image, blank=True, null=True,
                                       on_delete=models.SET_NULL)

    page = ParentalKey('website.HomePage', related_name='sponsors')

    panels = [
        FieldPanel('title'),
        FieldPanel('link'),
        ImageChooserPanel('logo'),
    ]

    class Meta:
        ordering = ['title']


class HomePage(Page):
    body = RichTextField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)

    # Sponsors
    template = 'layouts/website/homepage.jade'

    serve = views.homepage

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full title"),
    FieldPanel('twitter'),
    FieldPanel('facebook'),
    FieldPanel('email'),
    FieldPanel('github'),
    InlinePanel( HomePage, 'sponsors', label="Sponsors" ),
]