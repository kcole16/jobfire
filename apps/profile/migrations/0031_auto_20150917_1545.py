# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0030_auto_20150917_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='total_funding',
            field=models.BigIntegerField(null=True),
        ),
    ]
