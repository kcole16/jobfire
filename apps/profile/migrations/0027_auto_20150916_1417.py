# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0026_auto_20150915_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='about',
            field=models.CharField(max_length=1400),
        ),
    ]
