# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0009_auto_20150803_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='email_ext',
            field=models.CharField(default='virginia.edu', max_length=30),
            preserve_default=False,
        ),
    ]
