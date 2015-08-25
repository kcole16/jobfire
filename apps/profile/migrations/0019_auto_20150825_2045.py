# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0018_auto_20150823_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='graduation_date',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.ForeignKey(to='profile.Major', null=True),
        ),
    ]
