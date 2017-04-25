# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_myproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale_active',
            field=models.BooleanField(default=False),
        ),
    ]
