# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_auto_20150803_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='job_start_date',
            field=models.CharField(max_length=100, choices=[(b'immediate', b'Immediate'), (b'flexible', b'Flexible')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='job_type',
            field=models.CharField(max_length=100, choices=[(b'full-time', b'Full-Time'), (b'part-time', b'Part-Time'), (b'internship', b'Internship')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='role',
            field=models.CharField(max_length=100, choices=[(b'engineering', b'Engineering'), (b'product', b'product'), (b'business', b'business')]),
        ),
    ]
