# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-01 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedal',
            name='destino',
            field=models.TextField(default=''),
        ),
    ]
