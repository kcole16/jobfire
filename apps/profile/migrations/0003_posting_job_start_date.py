# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20150724_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='job_start_date',
            field=models.CharField(default='Flexible', max_length=100),
            preserve_default=False,
        ),
    ]
