# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('start_datetime', models.DateTimeField(verbose_name='Start')),
                ('end_datetime', models.DateTimeField(verbose_name='End')),
                ('signup_link', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventIndex',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('time', models.TimeField()),
                ('speaker', models.CharField(max_length=255, blank=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='schedule', to='events.Event')),
            ],
            options={
                'ordering': ['time'],
            },
            bases=(models.Model,),
        ),
    ]
