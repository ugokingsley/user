# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jplaceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=1)),
                ('followers', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
