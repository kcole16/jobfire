# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0021_company_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
