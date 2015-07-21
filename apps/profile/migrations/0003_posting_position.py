# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20150721_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='position',
            field=models.CharField(default='Engineer', max_length=100),
            preserve_default=False,
        ),
    ]
