# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-22 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20170531_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
            preserve_default=False,
        ),
    ]