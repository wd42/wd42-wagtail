from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from tahuneairwalk.website.models import HomePage, ContentPage
from wagtail.wagtailcore.models import Site


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        site = Site.objects.filter(is_default_site=True).first()

        root_page = site.root_page
        homepage = HomePage(
            title='Tahune AirWalk',

            page_ptr=root_page,
            content_type=ContentType.objects.get_for_model(HomePage),
            **{field.name: getattr(root_page, field.name)
               for field in root_page._meta.fields
               if field.name not in ['content_type', 'title']})
        homepage.save()

        site.root_page.add_child(instance=ContentPage(
            title='About us',
            slug='about-us',
            show_in_menus=True,
        ))