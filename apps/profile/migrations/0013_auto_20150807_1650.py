# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0012_auto_20150807_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='job_type',
            field=models.CharField(max_length=100, choices=[(b'Full-time', b'Full-Time'), (b'Internship (Summer)', b'Internship (Summer)'), (b'Internship (School Year)', b'Internship (School Year)')]),
        ),
    ]
