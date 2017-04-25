# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20170414_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='conditionTags',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='conditionWear',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='itemType',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
