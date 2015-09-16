# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0028_auto_20150916_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.IntegerField(null=True),
        ),
    ]
