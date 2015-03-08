# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='reportable',
            field=models.BooleanField(verbose_name='Reportable', default=False),
            preserve_default=True,
        ),
    ]
