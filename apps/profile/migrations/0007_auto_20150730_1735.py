# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_auto_20150730_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='description',
            field=models.TextField(),
        ),
    ]
