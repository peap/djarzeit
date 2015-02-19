# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('week', models.IntegerField(db_index=True, verbose_name='Week')),
                ('year', models.IntegerField(db_index=True, verbose_name='Year')),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name='Start Time')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('notes', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Notes')),
            ],
            options={
                'ordering': ['-start'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('archived', models.BooleanField(default=False, verbose_name='Archived')),
                ('category', models.ForeignKey(to='categories.Category')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='interval',
            name='timer',
            field=models.ForeignKey(to='timers.Timer'),
            preserve_default=True,
        ),
    ]
