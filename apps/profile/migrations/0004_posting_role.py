# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_posting_job_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='role',
            field=models.CharField(default='Engineering', max_length=100),
            preserve_default=False,
        ),
    ]
