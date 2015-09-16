# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0027_auto_20150916_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='funding_stage',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='growth',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='hype',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='total_funding',
            field=models.IntegerField(null=True),
        ),
    ]
