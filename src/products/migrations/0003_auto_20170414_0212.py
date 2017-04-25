# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20170414_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='msrp',
            field=models.DecimalField(default=8.88, max_digits=100, decimal_places=2),
        ),
        migrations.AddField(
            model_name='product',
            name='photos',
            field=models.FileField(default=1, upload_to=b'uploads/%Y/%m/%d/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='style',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
