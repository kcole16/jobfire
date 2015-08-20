# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0015_auto_20150820_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='linkedin_photo',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
