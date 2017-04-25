# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20170416_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='type',
            field=models.CharField(default=b'hd', max_length=20, choices=[(b'hd', b'HD'), (b'sd', b'SD'), (b'micro', b'Micro')]),
        ),
        migrations.AlterField(
            model_name='thumbnail',
            name='media',
            field=models.ImageField(height_field=b'height', width_field=b'width', upload_to=products.models.thumbnail_location),
        ),
    ]
