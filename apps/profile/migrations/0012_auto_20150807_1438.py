# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0011_auto_20150804_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='industries',
        ),
        migrations.AddField(
            model_name='student',
            name='graduation_date',
            field=models.CharField(default='Spring 2015', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='linkedin',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='portfolio',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='posting',
            name='job_start_date',
            field=models.CharField(max_length=100, choices=[(b'Immediate', b'Immediate'), (b'Flexible', b'Flexible')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='job_type',
            field=models.CharField(max_length=100, choices=[(b'Full-time', b'Full-Time'), (b'Part-time', b'Part-Time'), (b'Internship', b'Internship')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='role',
            field=models.CharField(max_length=100, choices=[(b'Engineering', b'Engineering'), (b'Product', b'Product'), (b'Business', b'Business')]),
        ),
    ]
