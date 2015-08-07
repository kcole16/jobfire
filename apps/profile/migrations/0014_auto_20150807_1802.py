# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0013_auto_20150807_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='linkedin',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='portfolio',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
