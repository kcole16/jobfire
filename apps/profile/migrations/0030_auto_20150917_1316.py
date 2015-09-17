# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0029_company_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='funding_stage',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
