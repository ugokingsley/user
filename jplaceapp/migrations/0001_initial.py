# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTestimony',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testimony', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SharedTestimonies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('votes', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('testimonies', models.ForeignKey(to='jplaceapp.MyTestimony')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='testimony',
            field=models.ManyToManyField(to='jplaceapp.Testimonies'),
        ),
        migrations.AddField(
            model_name='sharedtestimonies',
            name='testimony',
            field=models.ForeignKey(to='jplaceapp.Testimonies', unique=True),
        ),
        migrations.AddField(
            model_name='sharedtestimonies',
            name='users_voted',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
