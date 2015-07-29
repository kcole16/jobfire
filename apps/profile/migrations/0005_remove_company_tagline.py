# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_posting_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='tagline',
        ),
    ]
