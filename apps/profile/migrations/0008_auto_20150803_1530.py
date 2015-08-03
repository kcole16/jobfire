# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_auto_20150730_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='job_start_date',
            field=models.CharField(max_length=100, choices=[(b'immediate', b'immediate'), (b'flexible', b'flexible')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='job_type',
            field=models.CharField(max_length=100, choices=[(b'full-time', b'full-time'), (b'part-time', b'part-time'), (b'internship', b'internship')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='role',
            field=models.CharField(max_length=100, choices=[(b'engineering', b'engineering'), (b'product', b'product'), (b'business', b'business')]),
        ),
    ]
