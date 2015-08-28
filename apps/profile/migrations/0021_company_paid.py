# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0020_auto_20150825_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
