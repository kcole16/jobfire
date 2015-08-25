# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0019_auto_20150825_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='linkedin',
            field=models.CharField(default=b'(optional)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='portfolio',
            field=models.CharField(default=b'(optional)', max_length=100, null=True),
        ),
    ]
