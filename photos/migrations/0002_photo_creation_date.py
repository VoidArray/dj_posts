# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='creation_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
