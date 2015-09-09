# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0024_market'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='profile.Company')),
            ],
        ),
        migrations.AddField(
            model_name='posting',
            name='started',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='follow',
            name='posting',
            field=models.ForeignKey(to='profile.Posting'),
        ),
        migrations.AddField(
            model_name='follow',
            name='student',
            field=models.ForeignKey(to='profile.Student'),
        ),
    ]
