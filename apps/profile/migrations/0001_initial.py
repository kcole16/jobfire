# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interview_granted', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('logo', models.FileField(upload_to=b'company/logos')),
                ('tagline', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100)),
                ('s3_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('application', models.ForeignKey(to='profile.Application')),
                ('company', models.ForeignKey(to='profile.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('job_type', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=400)),
                ('company', models.ForeignKey(to='profile.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('company', models.ForeignKey(to='profile.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('resume_s3', models.CharField(max_length=1000)),
                ('industries', models.ManyToManyField(to='profile.Industry')),
                ('major', models.ForeignKey(to='profile.Major')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('logo', models.FileField(upload_to=b'university/logos')),
                ('color_main', models.CharField(max_length=10)),
                ('color_secondary', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(to='profile.University'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posting',
            name='university',
            field=models.ForeignKey(to='profile.University'),
        ),
        migrations.AddField(
            model_name='interview',
            name='posting',
            field=models.ForeignKey(to='profile.Posting'),
        ),
        migrations.AddField(
            model_name='interview',
            name='student',
            field=models.ForeignKey(to='profile.Student'),
        ),
        migrations.AddField(
            model_name='document',
            name='student',
            field=models.ForeignKey(to='profile.Student'),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(to='profile.Industry'),
        ),
        migrations.AddField(
            model_name='company',
            name='universities',
            field=models.ManyToManyField(to='profile.University'),
        ),
        migrations.AddField(
            model_name='application',
            name='company',
            field=models.ForeignKey(to='profile.Company'),
        ),
        migrations.AddField(
            model_name='application',
            name='posting',
            field=models.ForeignKey(to='profile.Posting'),
        ),
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.ForeignKey(to='profile.Student'),
        ),
    ]
