# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jplaceapp', '0002_testimonies_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonies',
            name='image',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
