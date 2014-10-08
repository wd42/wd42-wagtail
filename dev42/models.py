import six

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from wagtail.wagtailcore import models as wagtailmodels
from wagtail.wagtailcore.query import PageQuerySet
from wagtail.wagtailsearch.backends import get_search_backend

from .utils.managers import SiblingsInOrderQuerySet


class PageBase(wagtailmodels.PageBase):
    def __init__(cls, name, bases, dct):
        super(PageBase, cls).__init__(name, bases, dct)

        if 'template' not in dct:
            cls.template = "%s/layouts/%s.jade" % (
                cls._meta.app_label, cls._meta.model_name)

        # Add page manager
        PageManager().contribute_to_class(cls, 'objects')


class PageQuerySet(wagtailmodels.PageQuerySet, SiblingsInOrderQuerySet):
    pass


class PageManager(wagtailmodels.PageManager):
    def get_queryset(self):
        return PageQuerySet(self.model).order_by('path')


class Page(six.with_metaclass(PageBase, wagtailmodels.Page)):
    # Disable the creation of the related field accessor on Page
    # This prevents conflicts with model names and field names
    page_ptr = models.OneToOneField(wagtailmodels.Page, parent_link=True,
                                    related_name='+')

    objects = PageManager()

    class Meta:
        abstract = True
    is_abstract = True
