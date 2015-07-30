# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_remove_company_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
