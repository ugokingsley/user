# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jplaceapp', '0003_auto_20170525_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exuserprofile',
            name='is_human',
        ),
        migrations.AddField(
            model_name='exuserprofile',
            name='picture',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'pic_folder/'),
        ),
    ]
