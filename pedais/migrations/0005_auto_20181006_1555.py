# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-06 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedais', '0004_pedal_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedal',
            name='grupo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pedais.Grupo'),
        ),
    ]
