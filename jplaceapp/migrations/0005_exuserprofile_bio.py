# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jplaceapp', '0004_auto_20170526_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='exuserprofile',
            name='bio',
            field=models.TextField(default=None, unique=True),
        ),
    ]
