# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0017_auto_20150820_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='resume_s3',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
