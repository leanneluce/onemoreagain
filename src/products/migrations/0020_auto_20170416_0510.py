# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20170416_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(upload_to=products.models.media_location),
        ),
    ]
