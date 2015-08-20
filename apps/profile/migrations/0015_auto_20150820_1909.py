# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0014_auto_20150807_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityPosting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='posting',
            name='job_type',
            field=models.CharField(db_index=True, max_length=100, choices=[(b'Full-time', b'Full-Time'), (b'Internship (Summer)', b'Internship (Summer)'), (b'Internship (School Year)', b'Internship (School Year)')]),
        ),
        migrations.AlterField(
            model_name='posting',
            name='location',
            field=models.CharField(max_length=100, db_index=True),
        ),
        migrations.AlterField(
            model_name='posting',
            name='role',
            field=models.CharField(db_index=True, max_length=100, choices=[(b'Engineering', b'Engineering'), (b'Product', b'Product'), (b'Business', b'Business')]),
        ),
        migrations.AddField(
            model_name='universityposting',
            name='posting',
            field=models.ForeignKey(to='profile.Posting'),
        ),
        migrations.AddField(
            model_name='universityposting',
            name='university',
            field=models.ForeignKey(to='profile.University'),
        ),
    ]
