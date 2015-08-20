# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0016_student_linkedin_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='linkedin_photo',
            new_name='picture',
        ),
    ]
