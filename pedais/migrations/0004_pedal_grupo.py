# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-06 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedais', '0003_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedal',
            name='grupo',
            field=models.TextField(default=''),
        ),
    ]
